# This file contains a context manager for handling database sessions.

from chalicelib.dddpy.shared.mysql.base import SessionLocal
from contextlib import contextmanager

# The session_scope function is a context manager that provides a transactional scope around a series of operations.
# It creates a new session, yields it for use in a transaction, and then commits the transaction if no exceptions occurred.
# If an exception did occur, it rolls back the transaction.
# Finally, it ensures the session is closed.
@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        # If an exception occurs, the transaction is rolled back.
        session.rollback()
        raise
    finally:
        # The session is closed whether an exception occurred or not.
        session.close()