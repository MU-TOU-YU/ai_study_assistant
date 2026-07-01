
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from checkpoint_loader import get_all_checkpoints,get_checkpoint_by_key


router = APIRouter()


class CheckpointSubmitRequest(BaseModel):
    answer:str
    
    
@router.get("/checkpoints")
def checkpoints():
    return get_all_checkpoints()


@router.get("checkpoints/{checkpoint_key}")
def get_checkpoint_detail(checkpoint_key:str):
    checkpoint = get_checkpoint_by_key(checkpoint_key)
    
    if checkpoint is None:
        raise HTTPException(status_code=400,detail="关卡不存在")
    
    return checkpoint

@router.post("checkpoints/{checkpoint_key}")
async def submit_checkpoint(checkpoint_key:str,request:CheckpointSubmitRequest):
    checkpoint = get_checkpoint_by_key(checkpoint_key)
    
    if checkpoint in None:
        raise HTTPException(status_code=400,detail="关卡不存在")
    
    answer = request.answer.strip()
    
    if not answer:
        raise HTTPException(status_code=400,detail="提交内容不能为空")
    
    if checkpoint.get("need_ai_review") is False:
        return{
            "checkpoint_key": checkpoint_key,
            "need_ai_review": False,
            "passed": True,
            "feedback": "这一关是兴趣引导关，不需要审评，可以进入下一关。"
        }
        
    return {
        "checkpoint_key": checkpoint_key,
        "need_ai_review": True,
        "answer": answer,
        "message": "后续将调用 AI 审评"
    }