# SQLAlchemy Model and Repository for Users
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, func
from typing import List, Optional
from library.dddpy.shared.mysql.base import Base
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.users.domain.users import Users, UsersRepository


class DBUsers(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=True)
    doc_identity = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    status = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class UsersMapper:
    
    @staticmethod
    def to_domain(db_user: DBUsers) -> Users:
        from library.dddpy.users.domain.users import Users
        return Users(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            email=db_user.email,
            password=db_user.password,
            doc_identity=db_user.doc_identity,
            phone=db_user.phone,
            status=db_user.status,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )


class UsersCmdRepositoryImpl(UsersRepository):
    
    def all(self) -> List[Users]:
        with session_scope() as session:
            db_users = session.query(DBUsers).all()
            return [UsersMapper.to_domain(db) for db in db_users]

    def create(self, data: dict) -> Users:
        with session_scope() as session:
            from library.dddpy.users.domain.users import UsersAlreadyExistsException
            
            existing = session.query(DBUsers).filter(
                DBUsers.email == data.get("email")
            ).first()
            if existing:
                raise UsersAlreadyExistsException(data.get("email"))
            
            db_user = DBUsers(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                password=data.get("password"),
                doc_identity=data.get("doc_identity"),
                phone=data.get("phone"),
                status=data.get("status", 1),
            )
            session.add(db_user)
            session.flush()
            session.refresh(db_user)
            return UsersMapper.to_domain(db_user)

    def update(self, id: int, data: dict) -> Users:
        with session_scope() as session:
            from library.dddpy.users.domain.users import UsersNotFoundException
            
            db_user = session.query(DBUsers).filter(
                DBUsers.id == id
            ).first()
            
            if not db_user:
                raise UsersNotFoundException(id)
            
            # Check for duplicate email if changing
            if data.get("email") and data.get("email") != db_user.email:
                existing = session.query(DBUsers).filter(
                    DBUsers.email == data.get("email"),
                    DBUsers.id != id
                ).first()
                if existing:
                    raise UsersAlreadyExistsException(data.get("email"))
            
            for key, value in data.items():
                if hasattr(db_user, key) and value is not None:
                    setattr(db_user, key, value)
            
            session.flush()
            session.refresh(db_user)
            return UsersMapper.to_domain(db_user)

    def delete(self, id: int) -> bool:
        with session_scope() as session:
            from library.dddpy.users.domain.users import UsersNotFoundException
            
            db_user = session.query(DBUsers).filter(
                DBUsers.id == id
            ).first()
            
            if not db_user:
                raise UsersNotFoundException(id)
            
            session.delete(db_user)
            return True

    def get_by_id(self, id: int) -> Users:
        with session_scope() as session:
            from library.dddpy.users.domain.users import UsersNotFoundException
            
            db_user = session.query(DBUsers).filter(
                DBUsers.id == id
            ).first()
            
            if not db_user:
                raise UsersNotFoundException(id)
            
            return UsersMapper.to_domain(db_user)

    def get_by_email(self, email: str) -> Users:
        with session_scope() as session:
            from library.dddpy.users.domain.users import UsersNotFoundException
            
            db_user = session.query(DBUsers).filter(
                DBUsers.email == email
            ).first()
            
            if not db_user:
                raise UsersNotFoundException()
            
            return UsersMapper.to_domain(db_user)


class UsersQueryRepositoryImpl(UsersRepository):
    
    def all(self) -> List[Users]:
        with session_scope() as session:
            db_users = session.query(DBUsers).all()
            return [UsersMapper.to_domain(db) for db in db_users]

    def create(self, data: dict):
        raise NotImplementedError("Use Command Repository")

    def update(self, id: int, data: dict):
        raise NotImplementedError("Use Command Repository")

    def delete(self, id: int):
        raise NotImplementedError("Use Command Repository")

    def get_by_id(self, id: int) -> Optional[Users]:
        with session_scope() as session:
            db_user = session.query(DBUsers).filter(
                DBUsers.id == id
            ).first()
            return UsersMapper.to_domain(db_user) if db_user else None

    def get_by_email(self, email: str) -> Optional[Users]:
        with session_scope() as session:
            db_user = session.query(DBUsers).filter(
                DBUsers.email == email
            ).first()
            return UsersMapper.to_domain(db_user) if db_user else None
