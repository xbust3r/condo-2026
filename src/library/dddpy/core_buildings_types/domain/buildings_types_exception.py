# Buildings Types Exceptions


class BuildingsTypesException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class BuildingsTypesNotFoundException(BuildingsTypesException):
    def __init__(self, type_id: int = None):
        message = f"Building Type with id {type_id} not found"
        super().__init__(message, status_code=404)


class BuildingsTypesAlreadyExistsException(BuildingsTypesException):
    def __init__(self, code: str):
        message = f"Building Type with code '{code}' already exists"
        super().__init__(message, status_code=409)
