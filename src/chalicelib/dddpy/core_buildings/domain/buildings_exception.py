from chalicelib.dddpy.shared.decorators.domain_exception import DomainException


class BuildingNotFoundException(DomainException):
    message = "Building not found"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=404)


class BuildingAlreadyExistsException(DomainException):
    message = "Building already exists"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=409)


class BuildingValidationException(DomainException):
    message = "Building validation failed"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=400)
