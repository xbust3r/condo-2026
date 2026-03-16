# Buildings Exceptions


class BuildingsException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class BuildingsNotFoundException(BuildingsException):
    def __init__(self, building_id: int = None):
        message = f"Building with id {building_id} not found"
        super().__init__(message, status_code=404)


class BuildingsAlreadyExistsException(BuildingsException):
    def __init__(self, code: str):
        message = f"Building with code '{code}' already exists"
        super().__init__(message, status_code=409)


class BuildingsCondominiumNotFoundException(BuildingsException):
    def __init__(self, condominium_id: int):
        message = f"Condominium with id {condominium_id} not found"
        super().__init__(message, status_code=400)
