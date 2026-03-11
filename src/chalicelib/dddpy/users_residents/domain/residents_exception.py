from chalicelib.dddpy.shared.decorators.domain_exception import DomainException


class ResidentNotFoundException(DomainException):
    message = "Resident not found"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=404)


class ResidentAlreadyExistsException(DomainException):
    message = "Resident already exists"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=409)


class ResidentValidationException(DomainException):
    message = "Resident validation failed"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=400)
