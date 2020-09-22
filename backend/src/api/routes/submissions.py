import subprocess
import os
import shutil
import json
from threading import Lock


from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form
from api import schemas, session, models, config, dramatiq
from api.database import worker_session

router = APIRouter()
build_lock = Lock()
test_lock = Lock()


def is_build_artifact(filename):
    return not (filename.endswith('.h') or filename.endswith('.cpp'))


@dramatiq.actor
def test_submission(build_result_id: int, job_id: int):
    with worker_session() as db:
        if not (build := db.query(models.BuildResult).get(build_result_id)):
            print(f'[Test ERROR] Build Result {build_result_id} DNE')
            return

        student_name = build.submission.student.name

        print(f'[Test {student_name}] Test submission')
        if job := db.query(models.ActiveJob).get(job_id):
            job.status = 'testing'
            job.save(db)

        working_dir = os.path.join(config.UPLOAD_DIR, build.submission.path)  # Abs path

    # Long Running Task
    report_name = os.path.join(working_dir, 'report.json')
    with test_lock:
        with open(f'{working_dir}/stdout.log', 'w') as stdout, open(f'{working_dir}/stderr.log', 'w') as stderr:
            process = subprocess.run(
                [f'{working_dir}/fcts_unittest --gtest_output="json:{report_name}"'],
                stdout=stdout,
                stderr=stderr,
                shell=True
            )

    with worker_session() as db:
        result = models.TestResult(
            build_result_id=build_result_id,
            exit_code=process.returncode,
            # error_message=process.stderr
        )

        if job := db.query(models.ActiveJob).get(job_id):
            job.delete(db)

        print(f'[Test {student_name}] Returned with exit code {result.exit_code}')
        if result.exit_code == 0:
            assert os.path.exists(report_name)

            with open(report_name) as fp:
                data = json.load(fp)

            result.total_tests = data['tests']
            result.failures = data['failures']
            result.errors = data['errors']
            result.json_report_path = os.path.relpath(report_name, config.UPLOAD_DIR)
        result.save(db)


@dramatiq.actor
def build_submission(submission_id: int, job_id: int):

    with worker_session() as db:
        if not (submission := db.query(models.Submission).get(submission_id)):
            print(f'[BUILD ERROR] Submission {submission_id} DNE')
            return

        working_dir = os.path.join(config.UPLOAD_DIR, submission.path)
        if job := db.query(models.ActiveJob).get(job_id):
            job.status = 'building'
            job.save(db)

        student_name = submission.student.name
        if build := submission.build_result:
            build.delete(db)
            [os.remove(fp) for f in os.listdir(working_dir) if os.path.isfile(fp := os.path.join(working_dir, f)) and is_build_artifact(f)]

        makefile = os.path.join(config.UPLOAD_DIR, 'Makefile')
        shutil.copyfile(makefile, os.path.join(working_dir, 'Makefile'))
        print(f'[BUILD {student_name}] Building submission')

    # Long Running Task
    with build_lock:
        process = subprocess.run([f'(cd {working_dir} && make)'], capture_output=True, text=True, shell=True)

    with worker_session() as db:
        result = models.BuildResult(
            submission_id=submission_id,
            exit_code=process.returncode,
            error_message=process.stderr
        ).save(db)

        print(f'[BUILD {student_name}] Returned with exit code {result.exit_code}')
        if result.exit_code == 0:

            if job := db.query(models.ActiveJob).get(job_id):
                job.status = 'queued'
                job.type = 'test'
                job.save(db)

            db.commit()
            test_submission.send_with_options(args=(result.id, job_id))
        else:
            if job := db.query(models.ActiveJob).get(job_id):
                job.delete(db)


def start_job(submission: models.Submission, db: Session):
    job = models.ActiveJob(
        name=submission.student.name,
        type='build'
    ).save(db)

    build_submission.send_with_options(args=(submission.id, job.id,), priority=10)


@router.post("/submissions/")
def build_all_submissions_route(db: Session = Depends(session)):
    [start_job(s, db) for s in db.query(models.Submission).all()]

    return 'ok'


@router.post("/submissions/{submission_id}")
def build_submission_route(submission_id, db: Session = Depends(session)):
    if submission := db.query(models.Submission).get(submission_id):
        start_job(submission, db)

    return 'ok'
