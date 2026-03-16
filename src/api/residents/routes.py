# FastAPI Router for Residents
from fastapi import APIRouter, HTTPException, status
from library.dddpy.users_residents.usecase import (
    CreateResidentsSchema,
    UpdateResidentsSchema,
    create_residents_usecase,
)
from library.dddpy.users_residents.domain import ResidentsNotFoundException
from library.dddpy.shared.schemas.response_schema import ResponseSchema

router = APIRouter(prefix="/residents", tags=["residents"])


@router.post("", response_model=ResponseSchema)
def create_resident(schema: CreateResidentsSchema):
    usecase = create_residents_usecase()
    resident = usecase.create(schema)
    return ResponseSchema(success=True, message="Resident created", data=resident.to_dict())


@router.get("", response_model=ResponseSchema)
def get_all_residents():
    usecase = create_residents_usecase()
    residents = usecase.get_all()
    return ResponseSchema(success=True, data=[r.to_dict() for r in residents])


@router.get("/by-user/{user_id}", response_model=ResponseSchema)
def get_residents_by_user(user_id: int):
    usecase = create_residents_usecase()
    residents = usecase.get_by_user(user_id)
    return ResponseSchema(success=True, data=[r.to_dict() for r in residents])


@router.get("/by-unity/{unity_id}", response_model=ResponseSchema)
def get_residents_by_unity(unity_id: int):
    usecase = create_residents_usecase()
    residents = usecase.get_by_unity(unity_id)
    return ResponseSchema(success=True, data=[r.to_dict() for r in residents])


@router.get("/{resident_id}", response_model=ResponseSchema)
def get_resident(resident_id: int):
    usecase = create_residents_usecase()
    try:
        resident = usecase.get_by_id(resident_id)
        return ResponseSchema(success=True, data=resident.to_dict())
    except ResidentsNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{resident_id}", response_model=ResponseSchema)
def update_resident(resident_id: int, schema: UpdateResidentsSchema):
    usecase = create_residents_usecase()
    try:
        resident = usecase.update(resident_id, schema)
        return ResponseSchema(success=True, message="Resident updated", data=resident.to_dict())
    except ResidentsNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{resident_id}", response_model=ResponseSchema)
def delete_resident(resident_id: int):
    usecase = create_residents_usecase()
    try:
        usecase.delete(resident_id)
        return ResponseSchema(success=True, message="Resident deleted")
    except ResidentsNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
