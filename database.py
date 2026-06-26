from datetime import datetime
from sqlalchemy import create_engine,Column,Integer,String,Text,DateTime
from sqlalchemy.orm import declarative_base,sessionmaker

DATABASE_URL = "sqlite:///./ai_stay.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

Base = declarative_base()

class AIRecord(Base):
    __tablename__ = "ai_records"
    
    id = Column(Integer,primary_key=True,index=True)
    filename = Column(String(255),nullable=False)
    task_type = Column(String(50),nullable=False)
    result = Column(Text,nullable=False)
    create_at = Column(DateTime,default=datetime.now)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def init_db():
    Base.metadata.create_all(
        bind=engine
    )
    
def save_ai_record(filename:str,task_type:str,result:str):
    db = SessionLocal()
    
    try:
        record = AIRecord(
            filename = filename,
            task_type = task_type,
            result = result
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return record
    
    except Exception:
        db.rollback()
        raise
        
    finally:    
        db.close()
        
def get_ai_records():
    db=SessionLocal()
    
    try:
        records=db.query(AIRecord).order_by(AIRecord.create_at.desc()).all()
        return records
    
    finally:
        db.close()
        
def get_ai_record_by_id(record_id:int):
    db=SessionLocal()
    
    try:
        record=db.query(AIRecord).filter(AIRecord.id == record_id).first()
        return record
    
    finally:
        db.close()        