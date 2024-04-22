from flask import Blueprint, request, jsonify
from helpers.token_validation import validateJWT
from helpers.utils import validateRequestTask
from models.task_model import Task
import controllers.task_controller as task_controller
import json


task = Blueprint("tasks", __name__)

@task.route("/v1/tasks/", methods=["POST"])
def create():
    try:
        token = validateJWT()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401

        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403
        
        if not request.data:
            raise 'Request error'

        payload = json.loads(request.data)

        if not validateRequestTask(payload):
            raise ValueError('Error validating form')

        newTask = Task()
        newTask.description = payload["description"]
        newTask.assignedToUid = payload["assignedToUid"]
        createdTask = task_controller.createTask(newTask, token)

        if createdTask == 'Not Found':
            raise ValueError('Assigned user not found!')
        
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    
    return jsonify({'id': str(createdTask.inserted_id)})

@task.route("/v1/tasks/createdby/", methods=["GET"])
def getCreatedTasks():
    try:
        token = validateJWT()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401

        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        tasks = jsonify(task_controller.tasksCreatedBy(token)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    return tasks

@task.route("/v1/tasks/assignedto/", methods=["GET"])
def getAssignedTasks():
    try:
        token = validateJWT()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401

        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403
        
        tasks = jsonify(task_controller.tasksAssignedTo(token)), 200

    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    return tasks

@task.route("/v1/tasks/<taskUid>", methods=["PATCH"])
def updateTask(taskUid):
    try:
        token = validateJWT()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401

        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        payload = json.loads(request.data)

        if 'done' not in payload:
            return jsonify({"error": 'Status done not found in the request'}), 400 

        taskUpdateAttempt = task_controller.updateTask(token, taskUid, payload["done"])

    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    return jsonify({'taskUid': str(taskUpdateAttempt["taskUid"])}), 200
    

@task.route("/v1/tasks/<taskUid>", methods=["DELETE"])
def deleteTask(taskUid):
    try:
        token = validateJWT()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401

        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        taskDeleteAttempt = task_controller.deleteTask(token, taskUid)

    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    return jsonify({'tasksAffected': taskDeleteAttempt.deleted_count}), 200
    