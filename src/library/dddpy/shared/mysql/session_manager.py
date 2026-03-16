# MySQL Session Manager
from library.dddpy.shared.mysql.base import SessionLocal
from contextlib import contextmanager


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
