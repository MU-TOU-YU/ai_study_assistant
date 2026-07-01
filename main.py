
from contextlib import asynccontextmanager
from database import init_db
from fastapi import FastAPI,Request
from utils import FileValidationError
from fastapi.responses import JSONResponse

from routers.file_mode import router as file_mode_router
from routers.records import router as records_router
from routers.checkpoint_mode import router as checkpoint_router


@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    print("[INFO]数据库初始化完成")
    yield
    print("[INFO]应用关闭")
    
    
app=FastAPI(lifespan=lifespan)


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

@app.exception_handler(RuntimeError)
async def runtime_error_handler(request:Request,exc:RuntimeError):
    """AI 上游服务调用失败 ->502 Bad Gateway"""
    print(f"[ERROR]上游服务器调用失败：{exc}")
    return JSONResponse(
        status_code=502,
        content={"detail":"AI服务暂时不可用,请稍候重试"}
    )

@app.get("/health")
def health_check():
    
    return {"status":"ok"}


app.include_router(file_mode_router,prefix="/file-mode",tags=["文件上传模式"])
app.include_router(records_router,tags=["历史记录"])
app.include_router(checkpoint_router,prefix="/checkpoint_mode",tags=["闯关模式"])