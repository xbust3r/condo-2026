from chalicelib.dddpy.shared.decorators.domain_exception import DomainException


class BuildingTypeNotFoundException(DomainException):
    message = "Building type not found"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=404)


class BuildingTypeAlreadyExistsException(DomainException):
    message = "Building type already exists"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=409)


class BuildingTypeValidationException(DomainException):
    message = "Building type validation failed"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=400)
