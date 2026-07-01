
from database import save_ai_record
from fastapi import UploadFile,File,APIRouter
from service.service_ai import summarize_text,generate_question,generate_study_plan
from utils import get_text_from_upload,build_response,validate_text_length,FileValidationError


router = APIRouter()


@router.post("/summarize")
async def summarize(file:UploadFile=File(...)):
    uploaded=await get_text_from_upload(file)
    validate_text=validate_text_length(uploaded.content)
    result=await summarize_text(validate_text)
    
    record = await save_ai_record(uploaded.filename,"summary",result)
    
    return build_response(record.id,uploaded.filename,"summarize",result)


@router.post("/question")
async def question(file:UploadFile=File(...)):
    uploaded=await get_text_from_upload(file)
    validate_text=validate_text_length(uploaded.content)
    result=await generate_question(validate_text)
    
    record = await save_ai_record(uploaded.filename,"question",result)
    
    return build_response(record.id,uploaded.filename,"generate_question",result) 

    
@router.post("/study_plan")
async def study_plan(file:UploadFile=File(...)):
    uploaded=await get_text_from_upload(file)
    validate_text=validate_text_length(uploaded.content)
    result=await generate_study_plan(validate_text)
    
    record = await save_ai_record(uploaded.filename,"study_plan",result)
    
    return build_response(record.id,uploaded.filename,"study_plan",result)