from chalicelib.dddpy.shared.decorators.domain_exception import DomainException


class CondominiumNotFoundException(DomainException):
    message = "Condominium not found"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=404)


class CondominiumAlreadyExistsException(DomainException):
    message = "Condominium already exists"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=409)


class CondominiumValidationException(DomainException):
    message = "Condominium validation failed"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=400)
