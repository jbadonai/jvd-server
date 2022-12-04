from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


database_url = "sqlite:///jvd.db"
engine = create_engine(database_url, connect_args={'check_same_thread':False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
