from datetime import datetime
from sqlalchemy import Column,Integer,String,Text,DateTime,select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./ai_stay.db"


engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False},
    echo=False
)


Base = declarative_base()


class AIRecord(Base):
    __tablename__ = "ai_records"
    
    id = Column(Integer,primary_key=True,index=True)
    filename = Column(String(255),nullable=False)
    task_type = Column(String(50),nullable=False)
    result = Column(Text,nullable=False)
    create_at = Column(DateTime,default=datetime.now)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    
async def save_ai_record(filename:str,task_type:str,result:str):
    async with AsyncSessionLocal() as db:
        record = AIRecord(
            filename=filename,
            task_type=task_type,
            result=result
        )
        db.add(record)
        
        await db.commit()
        
        return record
    
        
async def get_ai_records():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(AIRecord).order_by(AIRecord.create_at.desc())
        )
        return result.scalars().all()    
        
async def get_ai_record_by_id(record_id:int):
      async with AsyncSessionLocal() as db:
          return await db.get(AIRecord,record_id)      