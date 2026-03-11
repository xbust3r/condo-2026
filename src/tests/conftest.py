"""Pytest configuration and fixtures for condo-py tests."""
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch
import importlib

import pytest

# Add src to path
SRC_PATH = Path('/home/miguel/servers/condo-py/src')
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


@pytest.fixture(autouse=True)
def mock_database(monkeypatch):
    """Mock database connections to avoid real DB connections."""
    # Create mock objects
    mock_engine = MagicMock()
    mock_session = MagicMock()
    
    # Create a mock module to replace chalicelib.dddpy.shared.mysql.base
    mock_base_module = MagicMock()
    mock_base_module.create_engine = MagicMock(return_value=mock_engine)
    mock_base_module.sessionmaker = MagicMock(return_value=mock_session)
    mock_base_module.engine = mock_engine
    mock_base_module.SessionLocal = mock_session
    mock_base_module.Base = MagicMock()
    
    # Replace the module in sys.modules
    sys.modules['chalicelib.dddpy.shared.mysql.base'] = mock_base_module
    
    yield mock_session
    
    # Clean up
    if 'chalicelib.dddpy.shared.mysql.base' in sys.modules:
        del sys.modules['chalicelib.dddpy.shared.mysql.base']


@pytest.fixture
def datetime_now():
    """Return current datetime."""
    return datetime.now()


@pytest.fixture
def datetime_fixed():
    """Return a fixed datetime for testing."""
    return datetime(2025, 1, 1, 12, 0, 0)
