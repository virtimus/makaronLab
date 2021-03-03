

def isBlank(myString:str):
    return not (myString and myString.strip())

def isNotBlank(myString:str):
    return bool(myString and myString.strip())


def trim(myString:str):
    result = myString.strip() if myString != None else None
    return result


def replace(myString:str, search:str, replace:str):
    if myString == None:
        return myString
    return myString.replace(search,replace)

def toUpper(s:str):
    result = s.upper() if s!=None else None
    return result


def isSDigits(s:str):
    if s == None:
        return False
    result = s[1:].isdigit() if s.startswith('-') else s.isdigit()
    return result

def uuid():
    import uuid
    return uuid.uuid4()
        
    
        
