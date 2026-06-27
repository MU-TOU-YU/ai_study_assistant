import os
import asyncio
from openai import AsyncOpenAI,APIConnectionError,APITimeoutError,RateLimitError
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("DeepSeek_API_KEY")

client=AsyncOpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)


MAX_RETRIES = 2
RETRY_DELAY = 1.5

async def call_deepseek(prompt:str)->str:
    last_error=None
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = await client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role":"system",
                        "content":"你是一个ai学习助手,擅长帮初学者理解学习资料"
                    },
                    {
                        "role":"user",
                        "content":prompt
                    }
                ],
                max_tokens=800,
                temperature=0.3,
                timeout=30.0
            )
            
            if not response.choices:
                raise ValueError("API返回了空的choices")
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("API返回了空内容")
            return content

        except (APIConnectionError,APITimeoutError,RateLimitError) as e:
           last_error = e
           if attempt < MAX_RETRIES:
               sleep_time = RETRY_DELAY * (attempt + 1)
               print(f"[RETRY]第{attempt+1}次重试，等待{sleep_time}秒，原因{type(e).__name__}")
               await asyncio.sleep(sleep_time)
           else:
               raise RuntimeError(
                   f"DeepSeek API 调用失败,已重试{MAX_RETRIES}次，最后错误：{last_error}"
               ) from last_error
        
        except Exception as e:
            raise RuntimeError(
                f"DeepSeek API 调用失败:{type(e).__name__} - {e}"
            ) from e       
    
    
async def summarize_text(text:str)->str:
    prompt=f"""请用中文总结下面这份学习资料。

要求：
1. 用简洁语言概括主要内容
2. 提取 3-5 个核心知识点
3. 给出适合初学者的学习建议

资料内容：
{text[:8000]}
"""

    return await call_deepseek(prompt) 


async def generate_question(text:str)->str:
    prompt=f"""请根据下面的学习资料生成 5 道面试题。

要求：
1. 由浅入深
2. 每道题附带参考答案
3. 用中文输出

资料内容：
{text[:8000]}
"""

    return await call_deepseek(prompt)


async def generate_study_plan(text:str)->str:
    prompt=f"""请根据下面的学习资料，为初学者生成一份学习计划。

要求：
1. 按阶段划分
2. 每个阶段说明学习目标
3. 给出具体行动建议

资料内容：
{text[:8000]}
"""

    return await call_deepseek(prompt)
