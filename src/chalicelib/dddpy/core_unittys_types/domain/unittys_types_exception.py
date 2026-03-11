from chalicelib.dddpy.shared.decorators.domain_exception import DomainException


class UnityTypeNotFoundException(DomainException):
    message = "Unity type not found"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=404)


class UnityTypeAlreadyExistsException(DomainException):
    message = "Unity type already exists"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=409)


class UnityTypeValidationException(DomainException):
    message = "Unity type validation failed"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=400)
