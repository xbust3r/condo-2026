"""
Document mapper.
"""
from library.dddpy.core_documents.domain.document_entity import DocumentEntity
from library.dddpy.core_documents.infrastructure.dbdocument import DBDocument


class DocumentMapper:
    @staticmethod
    def to_domain(row: DBDocument) -> DocumentEntity:
        return DocumentEntity(
            id=row.id,
            uuid=row.uuid,
            condominium_id=row.condominium_id,
            uploader_user_id=row.uploader_user_id,
            title=row.title,
            description=row.description,
            file_url=row.file_url,
            file_size_bytes=row.file_size_bytes,
            mime_type=row.mime_type,
            category=row.category,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(row: DBDocument, uploader_name: str = None, condominium_name: str = None) -> DocumentEntity:
        entity = DocumentMapper.to_domain(row)
        entity.uploader_name = uploader_name
        entity.condominium_name = condominium_name
        return entity
