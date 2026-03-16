# FastAPI Router for Buildings Types
from fastapi import APIRouter, HTTPException, status
from library.dddpy.core_buildings_types.usecase import (
    CreateBuildingsTypesSchema,
    UpdateBuildingsTypesSchema,
    create_buildings_types_usecase,
)
from library.dddpy.core_buildings_types.domain import BuildingsTypesNotFoundException
from library.dddpy.shared.schemas.response_schema import ResponseSchema

router = APIRouter(prefix="/buildings-types", tags=["buildings-types"])


@router.post("", response_model=ResponseSchema)
def create_building_type(schema: CreateBuildingsTypesSchema):
    usecase = create_buildings_types_usecase()
    building_type = usecase.create(schema)
    return ResponseSchema(success=True, message="Building type created", data=building_type.to_dict())


@router.get("", response_model=ResponseSchema)
def get_all_building_types():
    usecase = create_buildings_types_usecase()
    types = usecase.get_all()
    return ResponseSchema(success=True, data=[t.to_dict() for t in types])


@router.get("/{type_id}", response_model=ResponseSchema)
def get_building_type(type_id: int):
    usecase = create_buildings_types_usecase()
    try:
        building_type = usecase.get_by_id(type_id)
        return ResponseSchema(success=True, data=building_type.to_dict())
    except BuildingsTypesNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{type_id}", response_model=ResponseSchema)
def update_building_type(type_id: int, schema: UpdateBuildingsTypesSchema):
    usecase = create_buildings_types_usecase()
    try:
        building_type = usecase.update(type_id, schema)
        return ResponseSchema(success=True, message="Building type updated", data=building_type.to_dict())
    except BuildingsTypesNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{type_id}", response_model=ResponseSchema)
def delete_building_type(type_id: int):
    usecase = create_buildings_types_usecase()
    try:
        usecase.delete(type_id)
        return ResponseSchema(success=True, message="Building type deleted")
    except BuildingsTypesNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
