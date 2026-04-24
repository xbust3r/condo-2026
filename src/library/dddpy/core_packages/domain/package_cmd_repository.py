"""Package command repository interface."""
class PackageCmdRepository:
    def create(self, entity: object) -> int: pass

    def update(self, entity: object) -> bool: pass

    def soft_delete(self, id: int) -> bool: pass

    def hard_delete(self, id: int) -> bool: pass
