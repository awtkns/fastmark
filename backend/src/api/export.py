import pandas as pd
import numpy as np

from api import schemas, worker_session, models, config, dramatiq


def get_test_results(submission: models.Submission) -> dict:
    if not submission.build_result or not submission.build_result.test_results:
        return dict()

    d = {}
    for test in submission.build_result.test_results:
        d[test.name + ' exit code'] = test.exit_code
        d[test.name + ' total tests'] = test.total_tests
        d[test.name + ' total failures'] = test.total_failures

    return d


def generate_results_report(assignment) -> bytes:
    submissions = [
        {
            'name': s.student.name,
            'd2l_id': s.student.d2l_id,
            'date': s.submission_datetime,
            'late': s.late,
            'overdue': s.overdue,
            'build exit_code': s.build_result.exit_code if s.build_result else np.NaN,
            **get_test_results(s)
        } for s in assignments.submissions
    ]

    df = pd.DataFrame.from_records(submissions)
    return bytes(df.to_csv(index=False), encoding='utf-8')
