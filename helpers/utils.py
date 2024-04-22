import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def checkEmail(email):
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False
 

def validateRequestUser(request: None):
    try:
        if 'email' not in request:
            return False
        
        if 'name' not in request:
            return False
        
        if 'password' not in request:
            return False

        return True

    except Exception as e:
        return (f'Raised exception: {e}')

def validateRequestTask(request: None):
    try:
        if 'description' not in request:
            return False
        
        if 'assignedToUid' not in request:
            return False

        return True

    except Exception as e:
        return (f'Raised exception: {e}')