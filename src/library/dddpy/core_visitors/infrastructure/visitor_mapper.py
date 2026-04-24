"""
Visitor mapper — maps between DB model and domain entity.
"""
from library.dddpy.core_visitors.infrastructure.dbvisitor import DBVisitor
from library.dddpy.core_visitors.domain.visitor_entity import VisitorEntity


class VisitorMapper:

    @staticmethod
    def to_domain(db_visitor: DBVisitor) -> VisitorEntity:
        return VisitorEntity(
            id=db_visitor.id,
            uuid=db_visitor.uuid,
            condominium_id=db_visitor.condominium_id,
            building_id=db_visitor.building_id,
            unit_id=db_visitor.unit_id,
            host_user_id=db_visitor.host_user_id,
            visitor_name=db_visitor.visitor_name,
            visitor_document_type=db_visitor.visitor_document_type,
            visitor_document_number=db_visitor.visitor_document_number,
            visitor_phone=db_visitor.visitor_phone,
            expected_date=db_visitor.expected_date,
            expected_time=db_visitor.expected_time,
            actual_checkin_at=db_visitor.actual_checkin_at,
            actual_checkout_at=db_visitor.actual_checkout_at,
            status=db_visitor.status,
            visit_purpose=db_visitor.visit_purpose,
            access_code=db_visitor.access_code,
            notes=db_visitor.notes,
            created_at=db_visitor.created_at,
            updated_at=db_visitor.updated_at,
            deleted_at=db_visitor.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(
        db_visitor: DBVisitor,
        host_user_full_name: str = None,
        unit_code: str = None,
        building_name: str = None,
        condominium_name: str = None,
    ) -> VisitorEntity:
        entity = VisitorMapper.to_domain(db_visitor)
        entity.host_user_full_name = host_user_full_name
        entity.unit_code = unit_code
        entity.building_name = building_name
        entity.condominium_name = condominium_name
        return entity