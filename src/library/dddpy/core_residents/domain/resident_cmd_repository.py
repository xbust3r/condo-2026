"""
Resident profile command repository — manage resident preferences.
"""
class ResidentProfileCmdRepository:
    """Manage resident profile preferences."""

    def create_or_update(self, entity: object) -> int:
        pass

    def update_preferences(self, user_id: int, condominium_id: int, preferences: dict) -> bool:
        pass

    def soft_delete(self, id: int) -> bool:
        pass
