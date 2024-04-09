from flask import request, jsonify
from app import webserver
from app import helper as hp

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
        Request handler for the get_results endpoint
    """
    job_id = int(job_id)

    # Check if job_id is valid
    if job_id not in webserver.tasks_runner.jobs:
        return jsonify({"error": "invalid job id"}), 405

    # Check if job_id is done and return the result
    status, result = webserver.tasks_runner.jobs[job_id]

    if status == "done":
        return jsonify({
            'status': 'done',
            'data': result
        })

    # If not, return running status
    return jsonify({'status': 'running'})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
        Request handler for the states_mean endpoint
    """
    # Get request data
    data = request.json
    data['type'] = hp.STATES_MEAN

    # Register job and increment job_id counter
    job_id = webserver.tasks_runner.register_job(data)

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
        Request handler for the state_mean endpoint
    """
    # Get request data
    data = request.json
    data['type'] = hp.STATE_MEAN

    # Register job and increment job_id counter
    job_id = webserver.tasks_runner.register_job(data)

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
        Request handler for the best5 endpoint
    """
    # Get request data
    data = request.json
    data['type'] = hp.BEST5

    # Register job and increment job_id counter
    job_id = webserver.tasks_runner.register_job(data)

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
        Request handler for the worst5 endpoint
    """
    # Get request data
    data = request.json
    data['type'] = hp.WORST5

    # Register job and increment job_id counter
    job_id = webserver.tasks_runner.register_job(data)

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
        Request handler for the global_mean endpoint
    """
    # Get request data
    data = request.json
    data['type'] = hp.GLOBAL_MEAN

    # Register job and increment job_id counter
    job_id = webserver.tasks_runner.register_job(data)

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
        Request handler for the diff_from_mean endpoint
    """
    # Get request data
    data = request.json
    data['type'] = hp.DIFF_FROM_MEAN

    # Register job and increment job_id counter
    job_id = webserver.tasks_runner.register_job(data)

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
        Request handler for the state_diff_from_mean endpoint
    """
    # Get request data
    data = request.json
    data['type'] = hp.STATE_DIFF_FROM_MEAN

    # Register job and increment job_id counter
    job_id = webserver.tasks_runner.register_job(data)

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
        Request handler for the mean_by_category_request endpoint
    """
    # Get request data
    data = request.json
    data['type'] = hp.MEAN_BY_CATEGORY

    # Register job and increment job_id counter
    job_id = webserver.tasks_runner.register_job(data)

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
        Request handler for the state_mean_by_category endpoint
    """
    # Get request data
    data = request.json
    data['type'] = hp.STATE_MEAN_BY_CATEGORY

    # Register job and increment job_id counter
    job_id = webserver.tasks_runner.register_job(data)

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown_request():
    """
        Request handler for the graceful_shutdown endpoint
    """
    webserver.tasks_runner.graceful_shutdown()
    return jsonify({"shutdown": "done"})

@webserver.route('/api/jobs', methods=['GET'])
def jobs_request():
    """
        Request handler for the jobs endpoint
    """
    jobs = []
    for job_id in webserver.tasks_runner.jobs:
        jobs.append({f"job_id_{job_id}": webserver.tasks_runner.jobs[job_id][0]})

    return jsonify(jobs)

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs_request():
    """
        Request handler for the num_jobs endpoint
    """
    num_jobs = 0
    for job_id in webserver.tasks_runner.jobs:
        if webserver.tasks_runner.jobs[job_id][0] == "running":
            num_jobs += 1

    return jsonify({"Num Jobs": num_jobs})
