from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import ProgrammingError
import os


VERBOSE = False

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://faux:genie@localhost:5434/dev")
PROJECT_SCHEMA = os.getenv("PROJECT_SCHEMA", "test_app")

engine = create_engine(
    DATABASE_URL,
    echo=VERBOSE,
)
Session = scoped_session(sessionmaker(bind=engine))

metadata_obj = MetaData(schema=PROJECT_SCHEMA)


def create_schema(engine, schema_name):
    """
    Creates a schema in the database if it does not already exist.

    :param engine: The SQLAlchemy engine to use for the connection.
    :param schema_name: The name of the schema to create.
    """
    with engine.connect() as conn:
        try:
            conn.execute(CreateSchema(schema_name, if_not_exists=True))
            conn.commit()
        except ProgrammingError as e:
            if "already exists" in str(e):
                pass  # Schema already exists, safe to proceed
            else:
                raise RuntimeError(f"Failed to create schema: {e}")


create_schema(engine, PROJECT_SCHEMA)


class Base(DeclarativeBase):
    """
    The base class for all declarative models in the project.

    Attributes:
        metadata (MetaData): The metadata object to use for the base class.
    """

    metadata = metadata_obj
