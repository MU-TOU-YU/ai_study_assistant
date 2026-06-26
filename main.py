
from database import init_db,save_ai_record,get_ai_records,get_ai_record_by_id
from fastapi import FastAPI,UploadFile,File,HTTPException,Request
from service.service_ai import summarize_text,generate_question,generate_study_plan
from utils import get_text_from_upload,build_response,get_save_filename,validate_text_length,FileValidationError
from fastapi.responses import JSONResponse


app=FastAPI()

#暂时(忽略FastAPI弃用警告)，后续改用lifespan
@app.on_event("startup")
def startup():
    init_db()


@app.exception_handler(FileValidationError)
async def file_validation_handler(request:Request,exc:FileValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail":str(exc)}
    )

@app.exception_handler(ValueError)
async def value_error_handler(request:Request,exc:ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail":str(exc)}
    )


@app.get("/health")
def health_check():
    
    return {"status":"ok"}

             
@app.post("/summarize")
async def summarize(file:UploadFile=File(...)):
    uploaded=await get_text_from_upload(file)
    validate_text=validate_text_length(uploaded.content)
    result=summarize_text(validate_text)
    
    record = save_ai_record(uploaded.filename,"summary",result)
    
    return build_response(record.id,uploaded.filename,"summarize",result)


@app.post("/question")
async def question(file:UploadFile=File(...)):
    uploaded=await get_text_from_upload(file)
    validate_text=validate_text_length(uploaded.content)
    result=generate_question(validate_text)
    
    record = save_ai_record(uploaded.filename,"question",result)
    
    return build_response(record.id,uploaded.filename,"generate_question",result) 

    
@app.post("/study_plan")
async def study_plan(file:UploadFile=File(...)):
    uploaded=await get_text_from_upload(file)
    validate_text=validate_text_length(uploaded.content)
    result=generate_study_plan(validate_text)
    
    record = save_ai_record(uploaded.filename,"study_plan",result)
    
    return build_response(record.id,uploaded.filename,"study_plan",result)


@app.get("/records")
def records():
    records=get_ai_records()
    
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
        
    
@app.get("/record/{record_id}")
def record_detail(record_id:int):
    record=get_ai_record_by_id(record_id)
    
    if record is None:
        raise HTTPException(status_code=404,detail="记录不存在")
    
    return {
            "id":record.id,
            "filename":record.filename,
            "task_type":record.task_type,
            "result":record.result,
            "create_at":record.create_at
        }
       