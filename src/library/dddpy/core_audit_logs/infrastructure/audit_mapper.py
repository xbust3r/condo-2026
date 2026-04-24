"""
AuditLog Mapper — transforms between DB model and domain entity.
"""
import json
from library.dddpy.core_audit_logs.infrastructure.dbaudit import DBAuditLog
from library.dddpy.core_audit_logs.domain.audit_log_entity import AuditLogEntity


class AuditLogMapper:
    """Mapper para convertir entre DBAuditLog y AuditLogEntity."""

    @staticmethod
    def to_domain(row: DBAuditLog) -> AuditLogEntity:
        old_vals = None
        new_vals = None
        if row.old_values:
            try:
                old_vals = json.loads(row.old_values)
            except Exception:
                old_vals = row.old_values
        if row.new_values:
            try:
                new_vals = json.loads(row.new_values)
            except Exception:
                new_vals = row.new_values

        return AuditLogEntity(
            id=row.id,
            uuid=row.uuid,
            user_id=row.user_id,
            action=row.action,
            resource_type=row.resource_type,
            resource_id=row.resource_id,
            resource_uuid=row.resource_uuid,
            old_values=old_vals,
            new_values=new_vals,
            ip_address=row.ip_address,
            user_agent=row.user_agent,
            created_at=row.created_at,
        )