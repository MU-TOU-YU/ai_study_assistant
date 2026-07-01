
from fastapi import APIRouter,HTTPException
from database import get_ai_records,get_ai_record_by_id


router = APIRouter()


@router.get("/records")
async def records():
    records=await get_ai_records()
    
    return[
        {
            "id":record.id,
            "filename":record.filename,
            "task_type":record.task_type,
            "result":record.result[:20],
            "create_at":record.create_at
        }
        for record in records
    ]                 
        
    
@router.get("/record/{record_id}")
async def record_detail(record_id:int):
    record=await get_ai_record_by_id(record_id)
    
    if record is None:
        raise HTTPException(status_code=404,detail="记录不存在")
    
    return {
            "id":record.id,
            "filename":record.filename,
            "task_type":record.task_type,
            "result":record.result,
            "create_at":record.create_at
        }