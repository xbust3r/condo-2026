"""
Audit log factory — writes immutable audit entries.
Used by other modules' usecases to record their actions.
"""
import json
from datetime import datetime
import uuid as uuid_lib

from library.dddpy.core_audit_logs.domain.audit_log_entity import AuditLogEntity
from library.dddpy.core_audit_logs.usecase.audit_cmd_schema import CreateAuditLogSchema
from library.dddpy.core_audit_logs.infrastructure.dbaudit import DBAuditLog
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("AuditFactory")


class AuditFactory:
    """
    Writes audit log entries.
    Called by other modules (charges, payments, announcements, etc.) after
    each write operation to maintain the audit trail.
    """

    @staticmethod
    def create_log(schema: CreateAuditLogSchema) -> int:
        """
        Write a single audit entry. Returns the new audit log id.
        This is the primary method used by other modules.
        """
        logger.info(
            f"Audit: user={schema.user_id} {schema.action} {schema.resource_type}:{schema.resource_id}"
        )
        with session_scope() as session:
            db_a = DBAuditLog(
                uuid=str(uuid_lib.uuid4()),
                user_id=schema.user_id,
                action=schema.action,
                resource_type=schema.resource_type,
                resource_id=schema.resource_id,
                resource_uuid=schema.resource_uuid,
                old_values=json.dumps(schema.old_values) if schema.old_values else None,
                new_values=json.dumps(schema.new_values) if schema.new_values else None,
                ip_address=schema.ip_address,
                user_agent=schema.user_agent,
            )
            session.add(db_a)
            session.flush()
            session.refresh(db_a)
            logger.debug(f"Audit log created id={db_a.id}")
            return db_a.id

    @staticmethod
    def log_action(
        user_id: int,
        action: str,
        resource_type: str,
        resource_id: int,
        resource_uuid: str,
        old_values: dict = None,
        new_values: dict = None,
        ip_address: str = None,
        user_agent: str = None,
    ) -> int:
        """
        Convenience method — creates a CreateAuditLogSchema internally.
        Use this when you already have the raw parameters.
        """
        schema = CreateAuditLogSchema(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_uuid=resource_uuid,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return AuditFactory.create_log(schema)