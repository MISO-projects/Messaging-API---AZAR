import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock SQLAlchemy before importing the application
mockdb = MagicMock()
mock_session = MagicMock()
mock_engine = MagicMock()
mockdb.session = mock_session
mockdb.engine = mock_engine
mockdb.create_all = MagicMock()

with patch('models.blacklist.db', mockdb):
    from application import application

@pytest.fixture
def app():
    app = application
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_db():
    return mockdb

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield 