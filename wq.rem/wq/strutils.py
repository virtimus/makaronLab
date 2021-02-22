

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
        
