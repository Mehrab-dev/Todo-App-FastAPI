from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

from core.settings import setting


engine = create_engine(
    setting.SQLALCHEMY_DATABASE_URL,
    connect_args = {"check_same_thread":False}
)

sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()