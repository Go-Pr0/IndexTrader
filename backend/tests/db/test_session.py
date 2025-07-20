from app.core.config import Settings
from app.db import session


def test_create_engines_and_sessions(mocker):
    """
    Test that the SQLAlchemy engines are created with the correct database URLs.
    """
    # Mock the settings object to provide controlled test URLs
    mock_settings = Settings(
        DATABASE_URL_USER="postgresql+psycopg://test_user:pw@host:5432/userdb",
        DATABASE_URL_GENERAL="postgresql+psycopg://test_general:pw@host:5432/generaldb",
    )
    mocker.patch("app.db.session.settings", mock_settings)

    # Mock create_engine to prevent actual engine creation and to spy on its calls
    mock_create_engine = mocker.patch("app.db.session.create_engine")

    # Call the initialization function to trigger the engine creation
    session.initialize_database_connections()

    # Assert that create_engine was called for both databases with the correct URLs
    assert mock_create_engine.call_count == 2
    mock_create_engine.assert_any_call(
        str(mock_settings.DATABASE_URL_USER),
        pool_pre_ping=True,
        json_serializer=session.json_serializer,
        json_deserializer=session.json_deserializer,
    )
    mock_create_engine.assert_any_call(
        str(mock_settings.DATABASE_URL_GENERAL),
        pool_pre_ping=True,
        json_serializer=session.json_serializer,
        json_deserializer=session.json_deserializer,
    )

    # Assert that sessionmakers are created and bound to the (mocked) engines
    assert session.SessionLocalUser is not None
    assert session.SessionLocalGeneral is not None
    assert session.SessionLocalUser.kw["bind"] is not None
    assert session.SessionLocalGeneral.kw["bind"] is not None 