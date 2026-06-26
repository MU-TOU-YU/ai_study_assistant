from fastapi import UploadFile
from pathlib import Path
from dataclasses import dataclass


#自定义异常，作为纯工具模块不依赖web框架，纯python
class FileValidationError(Exception):
    pass


@dataclass
class Uploadtext:
    filename:str
    content:str
    encoding:str
    byte_size:int


async def get_text_from_upload(file:UploadFile)->str:
    
    filename=get_save_filename(file)
    content=await file.read()
    encoding,text=detection_coding(content)
    
    return Uploadtext(
        filename=filename,
        content=text,
        encoding=encoding,
        byte_size=len(content)
    ) 
       

#编码检测部分
#按照优先级排列
_FALLBACK_ENCODINGS = [
    "utf-8",  #现代标准
    "gb18030",  #中国国标
    "gbk",  #中文windows默认
    "big5",  #繁体中文
    "shift_jis",#日文
    "euc-kr",  #韩文
    "latin-1"  #万能兜底器，垃圾桶编码
]

def detection_coding(content:bytes)->tuple[str,str]:
    errors = []
    
    for encoding in _FALLBACK_ENCODINGS:
        try:
            text = content.decode(encoding)
            return encoding,text
        except(UnicodeDecodeError,LookupError) as e:
            errors.append(f"{encoding}:{type(e).__name__}")
            
    raise ValueError(
        f"无法解码文件内容。已尝试编码:{','.join(_FALLBACK_ENCODINGS)}"
        f"文件可能是二进制格式或损坏的文本文件"
    )          


#文本长度校验
MIN_TEXT_LENGTH = 50
MAX_TEXT_LENGTH = 50000
TRUNCATE_WARN_LENGTH = 8000

def validate_text_length(text:str)->str:
    text=text.strip()
    
    if len(text) == 0:
        raise FileValidationError("文件内容为空，请上传包含有效文本的文件")
    
    if len(text) < MIN_TEXT_LENGTH:
        raise FileValidationError(
            f"文本内容过短({len(text)}字符)，至少需要{MIN_TEXT_LENGTH}字符"
        )
        
    if len(text) > MAX_TEXT_LENGTH:
        raise FileValidationError(
            f"文本内容过长({len(text)}字符)，最多支持{MAX_TEXT_LENGTH}字符"
        )
    
    if len(text) > TRUNCATE_WARN_LENGTH:
        print(f"[WARN] 文本长度 {len(text)} 超过 API 最优长度 {TRUNCATE_WARN_LENGTH}，将被截断")
        
    return text        


def build_response(record_id:int,filename:str,task_type:str,result:str)->dict:
    return {
        "id":record_id,
        "filename":filename,
        "task_type":task_type,
        "result":result
    } 
    

def get_save_filename(file:UploadFile)->str:
    if not file.filename:
        raise FileValidationError("文件名不能为空")
    
    filename = Path(file.filename).name
    
    if not filename.lower().endswith(".txt"):
        raise FileValidationError("只支持txt文件")
    
    return filename           