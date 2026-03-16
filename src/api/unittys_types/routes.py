# FastAPI Router for Unit Types
from fastapi import APIRouter, HTTPException, status
from library.dddpy.core_unittys_types.usecase import (
    CreateUnittysTypesSchema,
    UpdateUnittysTypesSchema,
    create_unittys_types_usecase,
)
from library.dddpy.core_unittys_types.domain import UnittysTypesNotFoundException
from library.dddpy.shared.schemas.response_schema import ResponseSchema

router = APIRouter(prefix="/unit-types", tags=["unit-types"])


@router.post("", response_model=ResponseSchema)
def create_unit_type(schema: CreateUnittysTypesSchema):
    usecase = create_unittys_types_usecase()
    unit_type = usecase.create(schema)
    return ResponseSchema(success=True, message="Unit type created", data=unit_type.to_dict())


@router.get("", response_model=ResponseSchema)
def get_all_unit_types():
    usecase = create_unittys_types_usecase()
    types = usecase.get_all()
    return ResponseSchema(success=True, data=[t.to_dict() for t in types])


@router.get("/{type_id}", response_model=ResponseSchema)
def get_unit_type(type_id: int):
    usecase = create_unittys_types_usecase()
    try:
        unit_type = usecase.get_by_id(type_id)
        return ResponseSchema(success=True, data=unit_type.to_dict())
    except UnittysTypesNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{type_id}", response_model=ResponseSchema)
def update_unit_type(type_id: int, schema: UpdateUnittysTypesSchema):
    usecase = create_unittys_types_usecase()
    try:
        unit_type = usecase.update(type_id, schema)
        return ResponseSchema(success=True, message="Unit type updated", data=unit_type.to_dict())
    except UnittysTypesNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{type_id}", response_model=ResponseSchema)
def delete_unit_type(type_id: int):
    usecase = create_unittys_types_usecase()
    try:
        usecase.delete(type_id)
        return ResponseSchema(success=True, message="Unit type deleted")
    except UnittysTypesNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
