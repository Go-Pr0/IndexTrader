import os
from unittest.mock import patch

from app.core.config import Settings

def test_settings_load_from_env():
    """
    Test that Pydantic settings correctly load from environment variables.
    """
    # Define test database URLs
    test_user_db_url = "postgresql+psycopg://test_user:test_password@localhost:5432/test_userdb"
    test_general_db_url = "postgresql+psycopg://test_general:test_password@localhost:5432/test_generaldb"

    # Use patch to temporarily set environment variables
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL_USER": test_user_db_url,
            "DATABASE_URL_GENERAL": test_general_db_url,
        },
    ):
        # Instantiate settings inside the patch context to load from the mocked env
        settings = Settings()

        # Assert that the settings have been loaded correctly
        assert str(settings.DATABASE_URL_USER) == test_user_db_url
        assert str(settings.DATABASE_URL_GENERAL) == test_general_db_url 