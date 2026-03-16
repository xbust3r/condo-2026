# SQLAlchemy Model and Repository for Unitys
from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, Integer, DateTime, func, ForeignKey
from typing import List, Optional
from library.dddpy.shared.mysql.base import Base
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.core_unitys.domain.unitys import Unitys, UnitysRepository


class DBUnitys(Base):
    __tablename__ = "core_unitys"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    size = Column(DECIMAL(10, 2), nullable=True)
    percentage = Column(DECIMAL(5, 2), nullable=True)
    type = Column(String(100), nullable=True)
    floor = Column(Integer, nullable=True)
    unit = Column(String(50), nullable=True)
    building_id = Column(BigInteger, ForeignKey("core_buildings.id"), nullable=False)
    unity_type_id = Column(BigInteger, ForeignKey("core_unittys_types.id"), nullable=True)
    status = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class UnitysMapper:
    
    @staticmethod
    def to_domain(db_unity: DBUnitys) -> Unitys:
        from library.dddpy.core_unitys.domain.unitys import Unitys
        return Unitys(
            id=db_unity.id,
            name=db_unity.name,
            code=db_unity.code,
            description=db_unity.description,
            size=float(db_unity.size) if db_unity.size else None,
            percentage=float(db_unity.percentage) if db_unity.percentage else None,
            type=db_unity.type,
            floor=db_unity.floor,
            unit=db_unity.unit,
            building_id=db_unity.building_id,
            unity_type_id=db_unity.unity_type_id,
            status=db_unity.status,
            created_at=db_unity.created_at,
            updated_at=db_unity.updated_at,
        )


class UnitysCmdRepositoryImpl(UnitysRepository):
    
    def all(self) -> List[Unitys]:
        with session_scope() as session:
            db_unitys = session.query(DBUnitys).all()
            return [UnitysMapper.to_domain(db) for db in db_unitys]

    def create(self, data: dict) -> Unitys:
        with session_scope() as session:
            from library.dddpy.core_unitys.domain.unitys import UnitysAlreadyExistsException
            
            existing = session.query(DBUnitys).filter(
                DBUnitys.code == data.get("code")
            ).first()
            if existing:
                raise UnitysAlreadyExistsException(data.get("code"))
            
            db_unity = DBUnitys(
                name=data.get("name"),
                code=data.get("code"),
                description=data.get("description"),
                size=data.get("size"),
                percentage=data.get("percentage"),
                type=data.get("type"),
                floor=data.get("floor"),
                unit=data.get("unit"),
                building_id=data.get("building_id"),
                unity_type_id=data.get("unity_type_id"),
                status=data.get("status", 1),
            )
            session.add(db_unity)
            session.flush()
            session.refresh(db_unity)
            return UnitysMapper.to_domain(db_unity)

    def update(self, id: int, data: dict) -> Unitys:
        with session_scope() as session:
            from library.dddpy.core_unitys.domain.unitys import UnitysNotFoundException
            
            db_unity = session.query(DBUnitys).filter(
                DBUnitys.id == id
            ).first()
            
            if not db_unity:
                raise UnitysNotFoundException(id)
            
            for key, value in data.items():
                if hasattr(db_unity, key) and value is not None:
                    setattr(db_unity, key, value)
            
            session.flush()
            session.refresh(db_unity)
            return UnitysMapper.to_domain(db_unity)

    def delete(self, id: int) -> bool:
        with session_scope() as session:
            from library.dddpy.core_unitys.domain.unitys import UnitysNotFoundException
            
            db_unity = session.query(DBUnitys).filter(
                DBUnitys.id == id
            ).first()
            
            if not db_unity:
                raise UnitysNotFoundException(id)
            
            session.delete(db_unity)
            return True

    def get_by_id(self, id: int) -> Unitys:
        with session_scope() as session:
            from library.dddpy.core_unitys.domain.unitys import UnitysNotFoundException
            
            db_unity = session.query(DBUnitys).filter(
                DBUnitys.id == id
            ).first()
            
            if not db_unity:
                raise UnitysNotFoundException(id)
            
            return UnitysMapper.to_domain(db_unity)

    def get_by_code(self, code: str) -> Unitys:
        with session_scope() as session:
            from library.dddpy.core_unitys.domain.unitys import UnitysNotFoundException
            
            db_unity = session.query(DBUnitys).filter(
                DBUnitys.code == code
            ).first()
            
            if not db_unity:
                raise UnitysNotFoundException()
            
            return UnitysMapper.to_domain(db_unity)

    def get_by_building(self, building_id: int) -> List[Unitys]:
        with session_scope() as session:
            db_unitys = session.query(DBUnitys).filter(
                DBUnitys.building_id == building_id
            ).all()
            return [UnitysMapper.to_domain(db) for db in db_unitys]


class UnitysQueryRepositoryImpl(UnitysRepository):
    
    def all(self) -> List[Unitys]:
        with session_scope() as session:
            db_unitys = session.query(DBUnitys).all()
            return [UnitysMapper.to_domain(db) for db in db_unitys]

    def create(self, data: dict):
        raise NotImplementedError("Use Command Repository")

    def update(self, id: int, data: dict):
        raise NotImplementedError("Use Command Repository")

    def delete(self, id: int):
        raise NotImplementedError("Use Command Repository")

    def get_by_id(self, id: int) -> Optional[Unitys]:
        with session_scope() as session:
            db_unity = session.query(DBUnitys).filter(
                DBUnitys.id == id
            ).first()
            return UnitysMapper.to_domain(db_unity) if db_unity else None

    def get_by_code(self, code: str) -> Optional[Unitys]:
        with session_scope() as session:
            db_unity = session.query(DBUnitys).filter(
                DBUnitys.code == code
            ).first()
            return UnitysMapper.to_domain(db_unity) if db_unity else None

    def get_by_building(self, building_id: int) -> List[Unitys]:
        with session_scope() as session:
            db_unitys = session.query(DBUnitys).filter(
                DBUnitys.building_id == building_id
            ).all()
            return [UnitysMapper.to_domain(db) for db in db_unitys]
