# FastAPI Router for Unitys
from fastapi import APIRouter, HTTPException, status
from library.dddpy.core_unitys.usecase import (
    CreateUnitysSchema,
    UpdateUnitysSchema,
    create_unitys_usecase,
)
from library.dddpy.core_unitys.domain import UnitysNotFoundException
from library.dddpy.shared.schemas.response_schema import ResponseSchema

router = APIRouter(prefix="/unitys", tags=["unitys"])


@router.post("", response_model=ResponseSchema)
def create_unity(schema: CreateUnitysSchema):
    usecase = create_unitys_usecase()
    unity = usecase.create(schema)
    return ResponseSchema(success=True, message="Unity created", data=unity.to_dict())


@router.get("", response_model=ResponseSchema)
def get_all_unitys():
    usecase = create_unitys_usecase()
    unitys = usecase.get_all()
    return ResponseSchema(success=True, data=[u.to_dict() for u in unitys])


@router.get("/by-building/{building_id}", response_model=ResponseSchema)
def get_unitys_by_building(building_id: int):
    usecase = create_unitys_usecase()
    unitys = usecase.get_by_building(building_id)
    return ResponseSchema(success=True, data=[u.to_dict() for u in unitys])


@router.get("/{unity_id}", response_model=ResponseSchema)
def get_unity(unity_id: int):
    usecase = create_unitys_usecase()
    try:
        unity = usecase.get_by_id(unity_id)
        return ResponseSchema(success=True, data=unity.to_dict())
    except UnitysNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{unity_id}", response_model=ResponseSchema)
def update_unity(unity_id: int, schema: UpdateUnitysSchema):
    usecase = create_unitys_usecase()
    try:
        unity = usecase.update(unity_id, schema)
        return ResponseSchema(success=True, message="Unity updated", data=unity.to_dict())
    except UnitysNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{unity_id}", response_model=ResponseSchema)
def delete_unity(unity_id: int):
    usecase = create_unitys_usecase()
    try:
        usecase.delete(unity_id)
        return ResponseSchema(success=True, message="Unity deleted")
    except UnitysNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
