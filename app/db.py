from sqlmodel import create_engine
from app import settings

# Connection to database
connection_string: str = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)
engine = create_engine(connection_string, echo=True, connect_args={"sslmode": "require"}, pool_recycle=300)