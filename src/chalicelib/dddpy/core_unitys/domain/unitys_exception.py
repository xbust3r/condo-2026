from chalicelib.dddpy.shared.decorators.domain_exception import DomainException


class UnityNotFoundException(DomainException):
    message = "Unity not found"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=404)


class UnityAlreadyExistsException(DomainException):
    message = "Unity already exists"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=409)


class UnityValidationException(DomainException):
    message = "Unity validation failed"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=400)
