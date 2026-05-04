"""
Payment Proof domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class PaymentProofNotFound(DomainException):
    def __init__(self):
        super().__init__("Comprobante de pago no encontrado", status_code=404)


class PaymentProofAlreadyReviewed(DomainException):
    def __init__(self):
        super().__init__("El comprobante ya fue revisado", status_code=409)


class PaymentProofInvalidFileType(DomainException):
    def __init__(self, mime_type: str = ""):
        msg = (
            "Tipo de archivo no permitido. "
            "Solo se aceptan imágenes (JPG, PNG, WebP) y PDF."
        )
        if mime_type:
            msg = f"{msg} Recibido: {mime_type}"
        super().__init__(msg, status_code=400)


class PaymentProofFileTooLarge(DomainException):
    def __init__(self, max_mb: int = 10):
        super().__init__(
            f"El archivo excede el límite de {max_mb} MB",
            status_code=400,
        )


class PaymentProofValidationError(DomainException):
    def __init__(self, message: str = "Datos del comprobante inválidos"):
        super().__init__(message, status_code=400)
