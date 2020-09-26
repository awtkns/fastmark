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


@dramatiq.actor
def test_submission(build_result_id: int, job_id: int, solution=False):
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
    report_name = os.path.join(working_dir, f'{"solution" if solution else "submission"}_report.json')
    test_suite = 'solution_unittest' if solution else 'fcts_unittest'
    cmd = [f'{working_dir}/{test_suite} --gtest_output="json:{report_name}"']

    with test_lock:
        process = subprocess.run(cmd, capture_output=True, shell=True)

    with worker_session() as db:
        result = models.TestResult(
            build_result_id=build_result_id,
            name=test_suite,
            exit_code=process.returncode,
            stderr=process.stderr
        )

        if job := db.query(models.ActiveJob).get(job_id):
            job.delete(db)

        print(f'[Test {student_name}] Returned with exit code {result.exit_code}')
        if os.path.exists(report_name):
            with open(report_name) as fp:
                data = json.load(fp)
            # os.remove(report_name)

            result.total_tests = data['tests']
            result.total_failures = data['failures']
            result.total_errors = data['errors']
            result.json_report = data
        result.save(db)


def copy_artifacts(destination_folder):
    for f in os.listdir(config.ARTIFACTS_DIR):
        shutil.copyfile(os.path.join(config.ARTIFACTS_DIR, f), os.path.join(destination_folder, f))


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

        copy_artifacts(destination_folder=working_dir)
        print(f'[BUILD {student_name}] Building submission')

    # Long Running Task
    with build_lock:
        process = subprocess.run([f'(cd {working_dir} && touch * && make)'], capture_output=True, text=True, shell=True)

    with worker_session() as db:
        result = models.BuildResult(
            submission_id=submission_id,
            exit_code=process.returncode,
            error_message=process.stderr
        ).save(db)

        print(f'[BUILD {student_name}] Returned with exit code {result.exit_code}')

        if job := db.query(models.ActiveJob).get(job_id):
            job.delete(db)

        if result.exit_code == 0:
            solution_test_job = models.ActiveJob(name=student_name, status='queued', type='solution test').save(db)
            submission_test_job = models.ActiveJob(name=student_name, status='queued', type='submission test').save(db)
            db.commit()

            test_submission.send_with_options(args=(result.id, submission_test_job.id,))
            test_submission.send_with_options(args=(result.id, solution_test_job.id, True,))


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
