from chalicelib.dddpy.shared.decorators.domain_exception import DomainException


class UserNotFoundException(DomainException):
    message = "User not found"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=404)


class UserAlreadyExistsException(DomainException):
    message = "User already exists"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=409)


class UserValidationException(DomainException):
    message = "User validation failed"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=400)
