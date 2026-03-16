# SQLAlchemy Model and Repository for Residents
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, func, ForeignKey
from typing import List, Optional
from library.dddpy.shared.mysql.base import Base
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.users_residents.domain.residents import Residents, ResidentsRepository


class DBResidents(Base):
    __tablename__ = "users_residents"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    condominium_id = Column(BigInteger, ForeignKey("core_condominiums.id"), nullable=False)
    building_id = Column(BigInteger, ForeignKey("core_buildings.id"), nullable=False)
    unity_id = Column(BigInteger, ForeignKey("core_unitys.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    type = Column(String(100), nullable=False)  # Owner, Tenant, Family, Employee
    status = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class ResidentsMapper:
    
    @staticmethod
    def to_domain(db_resident: DBResidents) -> Residents:
        from library.dddpy.users_residents.domain.residents import Residents
        return Residents(
            id=db_resident.id,
            condominium_id=db_resident.condominium_id,
            building_id=db_resident.building_id,
            unity_id=db_resident.unity_id,
            user_id=db_resident.user_id,
            type=db_resident.type,
            status=db_resident.status,
            created_at=db_resident.created_at,
            updated_at=db_resident.updated_at,
        )


class ResidentsCmdRepositoryImpl(ResidentsRepository):
    
    def all(self) -> List[Residents]:
        with session_scope() as session:
            db_residents = session.query(DBResidents).all()
            return [ResidentsMapper.to_domain(db) for db in db_residents]

    def create(self, data: dict) -> Residents:
        with session_scope() as session:
            db_resident = DBResidents(
                condominium_id=data.get("condominium_id"),
                building_id=data.get("building_id"),
                unity_id=data.get("unity_id"),
                user_id=data.get("user_id"),
                type=data.get("type"),
                status=data.get("status", 1),
            )
            session.add(db_resident)
            session.flush()
            session.refresh(db_resident)
            return ResidentsMapper.to_domain(db_resident)

    def update(self, id: int, data: dict) -> Residents:
        with session_scope() as session:
            from library.dddpy.users_residents.domain.residents import ResidentsNotFoundException
            
            db_resident = session.query(DBResidents).filter(
                DBResidents.id == id
            ).first()
            
            if not db_resident:
                raise ResidentsNotFoundException(id)
            
            for key, value in data.items():
                if hasattr(db_resident, key) and value is not None:
                    setattr(db_resident, key, value)
            
            session.flush()
            session.refresh(db_resident)
            return ResidentsMapper.to_domain(db_resident)

    def delete(self, id: int) -> bool:
        with session_scope() as session:
            from library.dddpy.users_residents.domain.residents import ResidentsNotFoundException
            
            db_resident = session.query(DBResidents).filter(
                DBResidents.id == id
            ).first()
            
            if not db_resident:
                raise ResidentsNotFoundException(id)
            
            session.delete(db_resident)
            return True

    def get_by_id(self, id: int) -> Residents:
        with session_scope() as session:
            from library.dddpy.users_residents.domain.residents import ResidentsNotFoundException
            
            db_resident = session.query(DBResidents).filter(
                DBResidents.id == id
            ).first()
            
            if not db_resident:
                raise ResidentsNotFoundException(id)
            
            return ResidentsMapper.to_domain(db_resident)

    def get_by_user(self, user_id: int) -> List[Residents]:
        with session_scope() as session:
            db_residents = session.query(DBResidents).filter(
                DBResidents.user_id == user_id
            ).all()
            return [ResidentsMapper.to_domain(db) for db in db_residents]

    def get_by_unity(self, unity_id: int) -> List[Residents]:
        with session_scope() as session:
            db_residents = session.query(DBResidents).filter(
                DBResidents.unity_id == unity_id
            ).all()
            return [ResidentsMapper.to_domain(db) for db in db_residents]


class ResidentsQueryRepositoryImpl(ResidentsRepository):
    
    def all(self) -> List[Residents]:
        with session_scope() as session:
            db_residents = session.query(DBResidents).all()
            return [ResidentsMapper.to_domain(db) for db in db_residents]

    def create(self, data: dict):
        raise NotImplementedError("Use Command Repository")

    def update(self, id: int, data: dict):
        raise NotImplementedError("Use Command Repository")

    def delete(self, id: int):
        raise NotImplementedError("Use Command Repository")

    def get_by_id(self, id: int) -> Optional[Residents]:
        with session_scope() as session:
            db_resident = session.query(DBResidents).filter(
                DBResidents.id == id
            ).first()
            return ResidentsMapper.to_domain(db_resident) if db_resident else None

    def get_by_user(self, user_id: int) -> List[Residents]:
        with session_scope() as session:
            db_residents = session.query(DBResidents).filter(
                DBResidents.user_id == user_id
            ).all()
            return [ResidentsMapper.to_domain(db) for db in db_residents]

    def get_by_unity(self, unity_id: int) -> List[Residents]:
        with session_scope() as session:
            db_residents = session.query(DBResidents).filter(
                DBResidents.unity_id == unity_id
            ).all()
            return [ResidentsMapper.to_domain(db) for db in db_residents]
