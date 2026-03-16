# Condominium Domain Exceptions


class CondominiumException(Exception):
    """Base exception for Condominium module"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class CondominiumNotFoundException(CondominiumException):
    def __init__(self, condominium_id: int = None):
        message = f"Condominium with id {condominium_id} not found"
        super().__init__(message, status_code=404)


class CondominiumAlreadyExistsException(CondominiumException):
    def __init__(self, code: str):
        message = f"Condominium with code '{code}' already exists"
        super().__init__(message, status_code=409)


class CondominiumValidationException(CondominiumException):
    def __init__(self, message: str):
        super().__init__(message, status_code=422)
