import subprocess
import os
import shutil
import json

from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form
from api import schemas, session, models, config, dramatiq
from api.database import worker_session


router = APIRouter()


def is_build_artifact(filename):
    return not (filename.endswith('.h') or filename.endswith('.cpp'))


@dramatiq.actor
def test_submission(build_result_id, job_id):
    with worker_session() as db:
        if not (build := db.query(models.BuildResult).get(build_result_id)):
            print(f'[Test ERROR] Build Result {build_result_id} DNE')
            return

        print(f'[Test {build.submission.student.name}] Test submission in {os.getcwd()}')
        if job := db.query(models.ActiveJob).get(job_id):
            job.status = 'testing'
            job.save(db)

        os.chdir(build.submission.path)

    # Long Running Task
    report_name = 'report.json'
    process = subprocess.run([f'./fcts_unittest --gtest_output="json:{report_name}"'], capture_output=True, text=True, shell=True)

    with worker_session() as db:
        result = models.TestResult(
            build_result_id=build_result_id,
            exit_code=process.returncode,
            error_message=process.stderr
        )

        if job := db.query(models.ActiveJob).get(job_id):
            job.delete(db)

        print(f'[Test {build.submission.student.name}] Test return with exit code {results.exit_code}')
        if result.exit_code == 0:
            assert os.path.exists(report_name)

            with open(report_name) as fp:
                data = json.load(fp)

            result.total_tests = data['tests']
            result.failures = data['failures']
            result.errors = data['errors']
            result.json_report_path = report_name  # TODO: proper path
        result.save(db)


@dramatiq.actor
def build_submission(submission_id, job_id):

    with worker_session() as db:
        if not (submission := db.query(models.Submission).get(submission_id)):
            print(f'[BUILD ERROR] Submission {submission_id} DNE')
            return

        if job := db.query(models.ActiveJob).get(job_id):
            job.status = 'building'
            job.save(db)

        student_name = submission.student.name

        if build := submission.build_result:
            build.delete(db)
            [os.remove(fp) for f in os.listdir(submission.path) if os.path.isfile(fp := os.path.join(submission.path, f)) and is_build_artifact(f)]

        shutil.copyfile('Makefile', os.path.join(submission.path, 'Makefile'))
        os.chdir(submission.path)
        print(f'[BUILD {student_name}] Building submission in {os.getcwd()}')

    # Long Running Task
    process = subprocess.run(['make'], capture_output=True, text=True, shell=True)

    with worker_session() as db:
        result = models.BuildResult(
            submission_id=submission_id,
            exit_code=process.returncode,
            error_message=process.stderr
        ).save(db)

        print(f'[BUILD {student_name}] Returned with exit code {result.exit_code}')
        if result.exit_code == 0:

            if job := db.query(models.ActiveJob).get(job_id):
                job.status = 'queued for test'
                job.save(db)
            test_submission.send_with_options(args=(result.id, job_id))
        else:
            if job := db.query(models.ActiveJob).get(job_id):
                job.delete(db)


@router.post("/submissions/")
def build_all_submissions_route(db: Session = Depends(session)):
    for s in db.query(models.Submission).all():
        job = models.ActiveJob(
            name=s.student.name,
            type='build'
        ).save(db)

        build_submission.send_with_options(args=(s.id, job.id,))

    return 'ok'


@router.post("/submissions/{submission_id}")
def build_submission_route(submission_id, db: Session = Depends(session)):
    if submission := db.query(models.Submission).get(submission_id):
        job = models.ActiveJob(
            name=submission.student.name,
            type='build'
        ).save(db)

        build_submission.send_with_options(args=(submission_id, job.id,))

    return 'ok'
