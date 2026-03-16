from chalicelib.dddpy.shared.decorators.domain_exception import DomainException


class ExampleNotFound(DomainException):
    def __init__(self):
        super().__init__("Example not found", status_code=404)


class RepeatedExampleCode(DomainException):
    def __init__(self):
        super().__init__("Example code already exists", status_code=409)
