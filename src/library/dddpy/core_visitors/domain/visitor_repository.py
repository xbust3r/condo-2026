"""Visitor command repository ABC — write operations."""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_visitors.domain.visitor_entity import VisitorEntity


class VisitorRepository(ABC):
    """Interfaz de escritura para operaciones de modificación de visitors."""

    @abstractmethod
    def create(self, entity: VisitorEntity) -> VisitorEntity:
        pass

    @abstractmethod
    def update(self, id: int, entity: VisitorEntity) -> Optional[VisitorEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        pass

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        """Physical delete."""
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        """Restore a soft-deleted record: clears deleted_at."""
        pass

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[VisitorEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        pass