"""Package domain entity — DDD for package/maquil delivery management."""
from datetime import datetime
from typing import Dict, Any, Optional


class PackageStatus:
    PENDING = "pending"
    WITH_CONCIERGE = "with_concierge"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    ALL = {PENDING, WITH_CONCIERGE, DELIVERED, CANCELLED}


class PackageEntity:
    """
    Entidad de dominio para paquetes/maquils del condominio.
    """

    VALID_STATUSES = PackageStatus.ALL

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        unit_id: int,
        recipient_user_id: int,
        carrier: Optional[str] = None,
        tracking_number: Optional[str] = None,
        description: Optional[str] = None,
        status: str = PackageStatus.PENDING,
        received_at: Optional[datetime] = None,
        delivered_at: Optional[datetime] = None,
        pickup_code: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enrichment fields
        recipient_name: Optional[str] = None,
        unit_code: Optional[str] = None,
        building_name: Optional[str] = None,
        condominium_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.unit_id = unit_id
        self.recipient_user_id = recipient_user_id
        self.carrier = carrier
        self.tracking_number = tracking_number
        self.description = description
        self.status = status
        self.received_at = received_at
        self.delivered_at = delivered_at
        self.pickup_code = pickup_code
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.recipient_name = recipient_name
        self.unit_code = unit_code
        self.building_name = building_name
        self.condominium_name = condominium_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "unit_id": self.unit_id,
            "recipient_user_id": self.recipient_user_id,
            "carrier": self.carrier,
            "tracking_number": self.tracking_number,
            "description": self.description,
            "status": self.status,
            "received_at": self.received_at.isoformat() if self.received_at else None,
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
            "pickup_code": self.pickup_code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            # Enrichment
            "recipient_name": self.recipient_name,
            "unit_code": self.unit_code,
            "building_name": self.building_name,
            "condominium_name": self.condominium_name,
        }

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.deleted_at is None

    def is_pending(self) -> bool:
        return self.status == PackageStatus.PENDING and not self.is_deleted()

    def is_delivered(self) -> bool:
        return self.status == PackageStatus.DELIVERED
