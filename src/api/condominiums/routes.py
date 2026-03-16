# FastAPI Router for Condominiums
from fastapi import APIRouter, HTTPException, status
from library.dddpy.core_condominiums.usecase.cmd import CreateCondominiumCmdSchema, UpdateCondominiumCmdSchema
from library.dddpy.core_condominiums.usecase import create_condominium_usecase
from library.dddpy.core_condominiums.domain import CondominiumNotFoundException, CondominiumAlreadyExistsException
from library.dddpy.shared.schemas.response_schema import ResponseSchema

router = APIRouter(prefix="/condominiums", tags=["condominiums"])


@router.post("", response_model=ResponseSchema)
def create_condominium(schema: CreateCondominiumCmdSchema):
    usecase = create_condominium_usecase()
    try:
        condominium = usecase.create(schema)
        return ResponseSchema(success=True, message="Condominium created", data=condominium.to_dict())
    except CondominiumAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=ResponseSchema)
def get_all_condominiums():
    usecase = create_condominium_usecase()
    condominiums = usecase.get_all()
    return ResponseSchema(success=True, data=[c.to_dict() for c in condominiums])


@router.get("/{condominium_id}", response_model=ResponseSchema)
def get_condominium(condominium_id: int):
    usecase = create_condominium_usecase()
    try:
        condominium = usecase.get_by_id(condominium_id)
        return ResponseSchema(success=True, data=condominium.to_dict())
    except CondominiumNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{condominium_id}", response_model=ResponseSchema)
def update_condominium(condominium_id: int, schema: UpdateCondominiumCmdSchema):
    usecase = create_condominium_usecase()
    try:
        condominium = usecase.update(condominium_id, schema)
        return ResponseSchema(success=True, message="Condominium updated", data=condominium.to_dict())
    except CondominiumNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{condominium_id}", response_model=ResponseSchema)
def delete_condominium(condominium_id: int):
    usecase = create_condominium_usecase()
    try:
        usecase.delete(condominium_id)
        return ResponseSchema(success=True, message="Condominium deleted")
    except CondominiumNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
