from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./yontak.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# DB 세션 반환용 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 테이블 자동 생성용
def create_tables():
    from . import models  # 상대경로 또는 from app import models
    Base.metadata.create_all(bind=engine)
