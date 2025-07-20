from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Define global variables to hold the engines and session makers
engine_user: Engine | None = None
engine_general: Engine | None = None
SessionLocalUser: sessionmaker | None = None
SessionLocalGeneral: sessionmaker | None = None

def json_serializer(obj):
    return obj

def json_deserializer(obj):
    return obj

def initialize_database_connections():
    """Initializes the database engines and session makers."""
    global engine_user, engine_general, SessionLocalUser, SessionLocalGeneral

    engine_user = create_engine(
        str(settings.DATABASE_URL_USER),
        pool_pre_ping=True,
        json_serializer=json_serializer,
        json_deserializer=json_deserializer,
    )
    SessionLocalUser = sessionmaker(autocommit=False, autoflush=False, bind=engine_user)

    engine_general = create_engine(
        str(settings.DATABASE_URL_GENERAL),
        pool_pre_ping=True,
        json_serializer=json_serializer,
        json_deserializer=json_deserializer,
    )
    SessionLocalGeneral = sessionmaker(autocommit=False, autoflush=False, bind=engine_general)

# Initialize on import for the main application flow
initialize_database_connections()
