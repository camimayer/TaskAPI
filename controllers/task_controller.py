from bson import ObjectId
from database.__init__ import database 
import app_config as config

def createTask(task, token):
    taskCollection = database.dataBase[config.CONST_TASK_COLLECTION]
    userCollection = database.dataBase[config.CONST_USER_COLLECTION]

    try:
        assignedToUid = ObjectId(task.assignedToUid)
    except:
        return "Not Found"

    assignToUser = userCollection.find_one({'_id': assignedToUid})
    createdByUser = userCollection.find_one({'email': token["email"]})

    if assignToUser is None:
        return "Not Found"
    
    task.createdByUid = str(createdByUser["_id"])
    task.createdByName = createdByUser["name"]
    task.assignedToName  = assignToUser["name"]

    return taskCollection.insert_one(task.__dict__)

def tasksCreatedBy(token) -> list:
    try:
        taskCollection = database.dataBase[config.CONST_TASK_COLLECTION]
        userCollection = database.dataBase[config.CONST_USER_COLLECTION]

        createdByUser = userCollection.find_one({'email': token["email"]})
        tasks = []
        for task in taskCollection.find({'createdByUid': str(createdByUser["_id"])}):
            currentTask = {}

            currentTask.update({'taskUid': str(task['_id'])})
            currentTask.update({'assignedToUid': task['assignedToUid']})
            currentTask.update({'assignedToName': task['assignedToName']})
            currentTask.update({'createdByUid': task['createdByUid']})
            currentTask.update({'createdByName': task['createdByName']})
            currentTask.update({'description': task['description']})
            currentTask.update({'done': task['done']})
            tasks.append(currentTask)

        return {"allTasks" : tasks}
        
    except:
         raise ValueError('Error on getting tasks information')

def tasksAssignedTo(token) -> list:
    try:
        taskCollection = database.dataBase[config.CONST_TASK_COLLECTION]
        userCollection = database.dataBase[config.CONST_USER_COLLECTION]

        assignToUser = userCollection.find_one({'email': token["email"]})
        tasks = []
        for task in taskCollection.find({'assignedToUid': str(assignToUser["_id"])}):
            currentTask = {}

            currentTask.update({'taskUid': str(task['_id'])})
            currentTask.update({'assignedToUid': task['assignedToUid']})
            currentTask.update({'assignedToName': task['assignedToName']})
            currentTask.update({'createdByUid': task['createdByUid']})
            currentTask.update({'createdByName': task['createdByName']})
            currentTask.update({'description': task['description']})
            currentTask.update({'done': task['done']})
            tasks.append(currentTask)
        
        return {"allTasks" : tasks}
        
    except:
         raise ValueError('Error on getting tasks information')

def updateTask(token, taskId, done):
    try:
        taskCollection = database.dataBase[config.CONST_TASK_COLLECTION]
        userCollection = database.dataBase[config.CONST_USER_COLLECTION]

        taskToUpdate = taskCollection.find_one({'_id': ObjectId(str(taskId))})
        currentUser = userCollection.find_one({'email': token["email"]})

        if taskToUpdate is None:
            raise ValueError('Task not found')

        if taskToUpdate["assignedToUid"] != str(currentUser["_id"]):
            raise ValueError('Users can only change status when task is assigned to them.')

        taskCollection.update_one({"_id":taskToUpdate["_id"]}, {"$set": {"done": done}})

        taskUpdated = taskCollection.find_one({'_id': ObjectId(str(taskId))})
        
        response = {}
        response.update({'taskUid': str(taskUpdated['_id'])})

        return response
    except Exception as err:
         raise ValueError('Error on updating task: ' f'{err}')


def deleteTask(token, taskId):
    try:
        taskCollection = database.dataBase[config.CONST_TASK_COLLECTION]
        userCollection = database.dataBase[config.CONST_USER_COLLECTION]

        taskToDelete = taskCollection.find_one({'_id': ObjectId(str(taskId))})
        currentUser = userCollection.find_one({'email': token["email"]})

        if taskToDelete is None:
            raise ValueError('Task not found')

        if taskToDelete["createdByUid"] != str(currentUser["_id"]):
            raise ValueError('Users can only delete when task is created by them.')

        taskDeleted = taskCollection.delete_one({"_id":taskToDelete["_id"]})
        
        return taskDeleted

    except Exception as err:
         raise ValueError('Error on deleting task: ' f'{err}')