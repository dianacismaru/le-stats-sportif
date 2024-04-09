from app import webserver
from app import helper as hp
from flask import request, jsonify
import os
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")
        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    print(webserver.tasks_runner.jobs.keys())
    job_id = int(job_id)

    # Check if job_id is valid
    if ((job_id) not in webserver.tasks_runner.jobs.keys()):
        return jsonify({"error": "job invalid"}), 405
    
    # Check if job_id is done and return the result
    status, result = webserver.tasks_runner.jobs[job_id]
    print("status is " + status + "\n")
    if (status == "done"):
        print("e done!\n")
        return jsonify({
            'status': 'done',
            'data': result
        })

    # If not, return running status
    print("e running\n")
    return jsonify({'status': 'running'})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    data = request.json
    data['type'] = hp.STATES_MEAN
    print(f"Got request {data}")

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    job_id = webserver.tasks_runner.register_job(data)
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    # Get request data
    data = request.json
    data['type'] = hp.STATE_MEAN

    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    job_id = webserver.tasks_runner.register_job(data)
    return jsonify({"job_id": job_id})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # Get request data
    data = request.json
    data['type'] = hp.BEST5

    # Register job and return associated job_id
    job_id = webserver.tasks_runner.register_job(data)
    return jsonify({"job_id": job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # TODO
    # Get request data
    data = request.json
    data['type'] = hp.WORST5

    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    job_id = webserver.tasks_runner.register_job(data)
    return jsonify({"job_id": job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # TODO
    # Get request data
    data = request.json
    data['type'] = hp.GLOBAL_MEAN

    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    job_id = webserver.tasks_runner.register_job(data)
    return jsonify({"job_id": job_id})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # TODO
    # Get request data
    data = request.json
    data['type'] = hp.DIFF_FROM_MEAN

    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    job_id = webserver.tasks_runner.register_job(data)
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    data = request.json
    data['type'] = hp.STATE_DIFF_FROM_MEAN

    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    job_id = webserver.tasks_runner.register_job(data)
    return jsonify({"job_id": job_id})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    data = request.json
    data['type'] = hp.MEAN_BY_CATEGORY
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    job_id = webserver.tasks_runner.register_job(data)
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    data = request.json
    data['type'] = hp.STATE_MEAN_BY_CATEGORY
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    job_id = webserver.tasks_runner.register_job(data)
    return jsonify({"job_id": job_id})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
