"""
Test Data Registry.

Tracks records created during a test for debugging, cleanup, and audit.

Usage:
    registry = TestDataRegistry()
    registry.register("core_condominiums", condo.id, condo.uuid)
    registry.register("core_buildings", bldg.id, bldg.uuid)

    # Inspect
    print(registry.get_ids("core_condominiums"))  # [1, 2, 3]

    # Export to JSON (for CI reports)
    import json
    print(json.dumps(registry.all(), indent=2))

    # Clear all
    registry.clear()
"""
import json
from typing import Optional


class TestDataRegistry:
    """
    Tracks records created during a test for debugging and cleanup.

    Tables are grouped by name, each record stores id + optional uuid.
    """

    def __init__(self):
        self._data = {}  # {table_name: [{"id": int, "uuid": str|None}, ...]}

    def register(self, table: str, record_id: int, uuid: Optional[str] = None):
        """Register a single record."""
        if table not in self._data:
            self._data[table] = []
        self._data[table].append({"id": record_id, "uuid": uuid})

    def register_bulk(self, table: str, records: list[dict]):
        """
        Register multiple records at once.

        Args:
            table: table name
            records: list of {"id": ..., "uuid": ...} dicts
        """
        if table not in self._data:
            self._data[table] = []
        self._data[table].extend(records)

    def get_ids(self, table: str) -> list[int]:
        """Get all IDs registered for a table."""
        return [r["id"] for r in self._data.get(table, [])]

    def get_uuids(self, table: str) -> list[str]:
        """Get all UUIDs registered for a table."""
        return [r["uuid"] for r in self._data.get(table, []) if r["uuid"]]

    def get_records(self, table: str) -> list[dict]:
        """Get all record dicts for a table."""
        return list(self._data.get(table, []))

    def all(self) -> dict:
        """Return a copy of all registered data."""
        return dict(self._data)

    def clear(self):
        """Clear all registered records."""
        self._data.clear()

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string for reporting."""
        return json.dumps(self._data, indent=indent, default=str)

    def summary(self) -> str:
        """Human-readable summary of all registered records."""
        lines = ["TestDataRegistry summary:"]
        for table, records in self._data.items():
            ids = [r["id"] for r in records]
            lines.append(f"  {table}: {len(records)} records — IDs: {ids}")
        return "\n".join(lines)
