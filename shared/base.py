from schemas.error import ErrorSchema

def getError(title, description):
    error = ErrorSchema()
    error.title = title
    error.message = description
    return error