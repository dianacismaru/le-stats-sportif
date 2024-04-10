"""
    Module to define constants used in the application
"""
import json

STATES_MEAN = 1
STATE_MEAN = 2
BEST5 = 3
WORST5 = 4
GLOBAL_MEAN = 5
DIFF_FROM_MEAN = 6
STATE_DIFF_FROM_MEAN = 7
MEAN_BY_CATEGORY = 8
STATE_MEAN_BY_CATEGORY = 9

def write_result(job_id, data):
    """
        Writes the result of the job to a file
    """
    with open(f"results/{job_id}.json", "w", encoding='utf-8') as fout:
        fout.write(json.dumps(data))


def extract_result(job_id):
    """
        Extracts the result of the job from a file
    """
    with open(f"results/{job_id}.json", "r", encoding='utf-8') as fin:
        return json.loads(fin.read())
