from library.dddpy.shared.decorators.domain_exception import DomainException


class CondominiumNotFound(DomainException):
    def __init__(self):
        super().__init__("Condominium not found", status_code=404)


class RepeatedCondominiumCode(DomainException):
    def __init__(self):
        super().__init__("Condominium code already exists", status_code=409)


class InvalidCondominiumData(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)