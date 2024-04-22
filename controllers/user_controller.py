import asyncio
from flask.json import jsonify
from models.user_model import User
from datetime import datetime, timedelta
import random
import uuid
import bcrypt
import jwt
import app_config as config
from database.__init__ import database

def generateHashPassword(password) -> str:
  salt = bcrypt.gensalt()
  hashedPassword = bcrypt.hashpw(password.encode("utf-8"), salt )

  return hashedPassword

def createUser(userInformation) -> str:
    newUser = None
    try:
      newUser = User()

      newUser.name = userInformation['name'].lower()
      newUser.email = userInformation['email'].lower()
      newUser.password = generateHashPassword(userInformation['password'])

      collection = database.dataBase[config.CONST_USER_COLLECTION]

      if collection.find_one({'email': newUser.email}):
        return 'Duplicate User'
      
      createdUser = collection.insert_one(newUser.__dict__)
      return createdUser

    except Exception as e:
      raise ValueError('Error when creating new user:' f'{e}')


def loginUser(userInformation) -> str:
  try:
    email = userInformation['email'].lower()
    password = userInformation['password'].encode("utf-8")

    collection = database.dataBase[config.CONST_USER_COLLECTION]  

    currentUser = collection.find_one({'email': email})

    if not currentUser:
      return 'Invalid email'    

    if not bcrypt.checkpw(password, currentUser['password']):
      return 'Invalid password'
    
    loggedUser = {}
    loggedUser.update({'uid': str(currentUser['_id'])})
    loggedUser.update({'email': currentUser['email']})
    loggedUser.update({'name': currentUser['name']})
    
    expiration = datetime.utcnow() + timedelta(seconds=config.JWT_EXPIRATION)

    jwtData = { 'email': currentUser['email'],'id': str(currentUser['_id']), 'exp': expiration }

    jwtToReturn = jwt.encode(payload=jwtData, key=config.TOKEN_SECRET)

    return jsonify({'token': jwtToReturn, 'expiration': config.JWT_EXPIRATION, 'loggedUser': loggedUser})

  except Exception as e:
    raise ValueError('Error when trying to login the user:' f'{e}')

def fetchUsers():
  try:
    collection = database.dataBase[config.CONST_USER_COLLECTION]  

    users = []
    for user in collection.find():
      currentUser = {}
      currentUser.update({'uid': str(user['_id'])})
      currentUser.update({'email': user['email']})
      currentUser.update({'name': user['name']})
      users.append(currentUser)
    
    return {"allUsers" : users}

  except Exception as e:
    raise ValueError('Error when trying to login the user:' f'{e}')
