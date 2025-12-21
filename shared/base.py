from schemas.reponse_schema.error import ErrorSchema

def getError(title, description):
    error = ErrorSchema()
    error.title = title
    error.message = description
    return error