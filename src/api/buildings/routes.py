# FastAPI Router for Buildings
from fastapi import APIRouter, HTTPException, status
from library.dddpy.core_buildings.usecase import (
    CreateBuildingsSchema,
    UpdateBuildingsSchema,
    create_buildings_usecase,
)
from library.dddpy.core_buildings.domain import BuildingsNotFoundException
from library.dddpy.shared.schemas.response_schema import ResponseSchema

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.post("", response_model=ResponseSchema)
def create_building(schema: CreateBuildingsSchema):
    usecase = create_buildings_usecase()
    building = usecase.create(schema)
    return ResponseSchema(success=True, message="Building created", data=building.to_dict())


@router.get("", response_model=ResponseSchema)
def get_all_buildings():
    usecase = create_buildings_usecase()
    buildings = usecase.get_all()
    return ResponseSchema(success=True, data=[b.to_dict() for b in buildings])


@router.get("/by-condominium/{condominium_id}", response_model=ResponseSchema)
def get_buildings_by_condominium(condominium_id: int):
    usecase = create_buildings_usecase()
    buildings = usecase.get_by_condominium(condominium_id)
    return ResponseSchema(success=True, data=[b.to_dict() for b in buildings])


@router.get("/{building_id}", response_model=ResponseSchema)
def get_building(building_id: int):
    usecase = create_buildings_usecase()
    try:
        building = usecase.get_by_id(building_id)
        return ResponseSchema(success=True, data=building.to_dict())
    except BuildingsNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{building_id}", response_model=ResponseSchema)
def update_building(building_id: int, schema: UpdateBuildingsSchema):
    usecase = create_buildings_usecase()
    try:
        building = usecase.update(building_id, schema)
        return ResponseSchema(success=True, message="Building updated", data=building.to_dict())
    except BuildingsNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{building_id}", response_model=ResponseSchema)
def delete_building(building_id: int):
    usecase = create_buildings_usecase()
    try:
        usecase.delete(building_id)
        return ResponseSchema(success=True, message="Building deleted")
    except BuildingsNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
