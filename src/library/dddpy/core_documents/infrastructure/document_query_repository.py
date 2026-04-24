"""
from typing import Optional
Document Query Repository Implementation — with bulk enrichment.
"""
from typing import Optional, List, Tuple

from sqlalchemy import text

from library.dddpy.core_documents.domain.document_entity import DocumentEntity
from library.dddpy.core_documents.domain.document_query_repository import DocumentQueryRepository
from library.dddpy.core_documents.infrastructure.dbdocument import DBDocument
from library.dddpy.core_documents.infrastructure.document_mapper import DocumentMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("DocumentQueryRepository")


class DocumentQueryRepositoryImpl(DocumentQueryRepository):

    def _bulk_enrich(
        self,
        rows: List[DBDocument],
        uploader_names: dict = None,
        condo_names: dict = None,
    ) -> List[DocumentEntity]:
        return [
            DocumentMapper.to_domain_enriched(
                row,
                uploader_name=uploader_names.get(row.uploader_user_id) if uploader_names else None,
                condominium_name=condo_names.get(row.condominium_id) if condo_names else None,
            )
            for row in rows
        ]

    def _fetch_uploader_names(self, rows: List[DBDocument]) -> dict:
        if not rows:
            return {}
        ids = list({r.uploader_user_id for r in rows})
        with session_scope() as session:
            result = session.execute(
                text("""
                    SELECT u.id, COALESCE(CONCAT(p.first_name, ' ', p.last_name), u.email) AS full_name
                    FROM users u
                    LEFT JOIN user_profiles p ON p.user_id = u.id AND p.deleted_at IS NULL
                    WHERE u.id IN :ids
                """),
                {"ids": tuple(ids)},
            )
            return {row.id: row.full_name for row in result}

    def _fetch_condo_names(self, rows: List[DBDocument]) -> dict:
        if not rows:
            return {}
        ids = list({r.condominium_id for r in rows})
        with session_scope() as session:
            from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
            result = session.query(DBCondominium.id, DBCondominium.name).filter(
                DBCondominium.id.in_(ids)
            ).all()
            return dict(result)

    def get_by_id(self, id: int) -> Optional[DocumentEntity]:
        logger.debug(f"Fetching document by id={id}")
        with session_scope() as session:
            row = session.query(DBDocument).filter(
                DBDocument.id == id,
                DBDocument.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            un = self._fetch_uploader_names([row])
            cn = self._fetch_condo_names([row])
            return DocumentMapper.to_domain_enriched(row, un.get(row.uploader_user_id), cn.get(row.condominium_id))

    def get_by_uuid(self, uuid: str) -> Optional[DocumentEntity]:
        logger.debug(f"Fetching document by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBDocument).filter(
                DBDocument.uuid == uuid,
                DBDocument.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            un = self._fetch_uploader_names([row])
            cn = self._fetch_condo_names([row])
            return DocumentMapper.to_domain_enriched(row, un.get(row.uploader_user_id), cn.get(row.condominium_id))

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        category: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[DocumentEntity], int]:
        logger.debug(f"Listing documents skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBDocument)
            if not include_deleted:
                query = query.filter(DBDocument.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBDocument.condominium_id == condominium_id)
            if category:
                query = query.filter(DBDocument.category == category)

            total = query.count()
            rows = query.order_by(DBDocument.created_at.desc()).offset(skip).limit(limit).all()

            un = self._fetch_uploader_names(rows)
            cn = self._fetch_condo_names(rows)
            return self._bulk_enrich(rows, un, cn), total
