import subprocess
import os
import shutil
import json

from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form
from api import schemas, session, models, config, dramatiq

router = APIRouter()


@dramatiq.actor
def test_submission(build_result_id):
    print("Testing Build", build_result_id)

    db = next(session())
    build = db.query(models.BuildResult).get(build_result_id)

    os.chdir(build.submission.path)
    report_name = f'{build_result_id}.json'
    process = subprocess.run([f'./fcts_unittest --gtest_output="json:{report_name}"'], capture_output=True, text=True, shell=True)

    result = models.TestResult(
        build_result_id=build_result_id,
        exit_code=process.returncode,
        error_message=process.stderr
    )

    if result.exit_code == 0:
        assert os.path.exists(report_name)

        with open(report_name) as fp:
            data = json.load(fp)

        result.total_tests = data['tests']
        result.failures = data['failures']
        result.errors = data['errors']
        result.json_report_path = report_name # TODO: proper path

    result.save(db)
    db.commit()


@dramatiq.actor
def build_submission(submission_id):
    print("Building submission", submission_id)

    db = next(session())
    submission = db.query(models.Submission).get(submission_id)
    print(submission.build_result)

    if build := submission.build_result:
        print(build)
        build.delete(db)
        db.commit()

    shutil.copyfile('Makefile', os.path.join(submission.path, 'Makefile'))

    os.chdir(submission.path)
    process = subprocess.run(['make'], capture_output=True, text=True, shell=True)

    result = models.BuildResult(
        submission_id=submission_id,
        exit_code=process.returncode,
        error_message=process.stderr
    ).save(db)
    db.commit()

    if result.exit_code == 0:
        test_submission.send_with_options(args=(result.id,))


@router.post("/submissions/{submission_id}")
def build_submission_route(submission_id):
    build_submission.send_with_options(args=(submission_id,))

    return 'ok'
