import pytest
from application import create_app
from database import db


@pytest.fixture
def app():
    """Fixture to create a Flask application instance with the testing configuration."""
    # Create the Flask app with the testing configuration
    app = create_app()
    app.config.from_object('config.TestingConfig')  # Use the TestingConfig

    # Initialize the database for testing
    with app.app_context():
        db.create_all()  # Create all tables in the testing database
        # You can add any seeding here if needed

    yield app

    # Tear down and clean up the database after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Fixture to get the test client for sending HTTP requests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Fixture for running app commands in tests."""
    return app.test_cli_runner()
