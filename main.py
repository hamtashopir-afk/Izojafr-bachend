from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
from jafr_engine import full_jafr
from raml_engine import raml_analysis
import random

app = FastAPI(title="Jafr & Raml AI")

# --- ÊäÙíãÇÊ DeepSeek ---
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("˜áíÏ API ÏíÓí˜ ÊäÙíã äÔÏå ÇÓÊ.")

client = AsyncOpenAI(
    base_url="https://api.deepseek.com",
    api_key=DEEPSEEK_API_KEY,
)

# --- ãÏáåÇí ÏÇÏå ---
class JafrRequest(BaseModel):
    name: str
    mother_name: str
    question: str

class RamlRequest(BaseModel):
    name: str
    mother_name: str
    question: str

class AIRequest(BaseModel):
    name: str
    mother_name: str
    question: str
    method: str  # "jafr" íÇ "raml"

# --- ÊæÇÈÚ ˜ã˜í ---
async def get_ai_interpretation(prompt: str) -> str:
    """ÇÑÓÇá Èå DeepSeek ÈÑÇí ÊİÓíÑ äåÇíí"""
    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "Êæ í˜ ãİÓÑ ãÊÎÕÕ ÏÑ Úáæã ÓäÊí ÌİÑ æ Ñãá åÓÊí. ÈÑ ÇÓÇÓ äÊÇíÌ ãÍÇÓÈÇÊí¡ í˜ ÊİÓíÑ ÌÇãÚ¡ åãÏáÇäå æ ˜ÇÑÈÑÏí Èå ÒÈÇä İÇÑÓí ÇÑÇÆå ÈÏå. áÍä Êæ ÈÇíÏ ÂÑÇãÔÈÎÔ æ ÑÇåäãÇ ÈÇÔÏ. åÑÒ ÇÏÚÇí ŞØÚíÊ ä˜ä æ åãíÔå ÊÃ˜íÏ ˜ä ˜å Çíä ÊÍáíá ÕÑİÇğ äãÇÏíä ÇÓÊ."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ÎØÇ ÏÑ ÏÑíÇİÊ ÊİÓíÑ AI: {str(e)}"

# --- EndpointåÇ ---
@app.post("/api/jafr")
async def api_jafr(req: JafrRequest):
    """ãÍÇÓÈå ÌİÑ æ ÊİÓíÑ AI"""
    result = full_jafr(req.name, req.mother_name, req.question)
    
    prompt = f"""
    ˜ÇÑÈÑ ÈÇ äÇã "{req.name}" æ äÇã ãÇÏÑ "{req.mother_name}" ÓæÇá ÒíÑ ÑÇ ÑÓíÏå ÇÓÊ:
    "{req.question}"
    
    äÊÇíÌ ãÍÇÓÈÇÊ ÌİÑ:
    - ÚÏÏ ˜á: {result['total']}
    - ÌİÑ Ç˜ÈÑ (ãäÒá ŞãÑí): {result['akbar']['name']} - {result['akbar']['meaning']}
    - ÌİÑ ÇÕÛÑ (ÈÑÌ): {result['asghar']['name']} ({result['asghar']['element']}) - {result['asghar']['meaning']}
    - ÎáØ ÛÇáÈ: {result['akhlat']['khilt']} ({result['akhlat']['tab']})
    - ÌåÊ: {result['akhlat']['direction']}
    - İÕá: {result['akhlat']['season']}
    
    áØİÇğ ÈÑ ÇÓÇÓ Çíä ÏÇÏååÇ¡ í˜ ÊİÓíÑ ÌÇãÚ æ ÑÇå˜ÇÑ Úãáí ÈÑÇí ˜ÇÑÈÑ ÇÑÇÆå ÈÏå.
    """
    
    ai_text = await get_ai_interpretation(prompt)
    
    return {
        "method": "jafr",
        "numbers": result,
        "interpretation": ai_text,
        "disclaimer": "Çíä ÊÍáíá ÕÑİÇğ ÈÑÇí ÓÑÑãí æ ÂãæÒÔ ÇÓÊ. ÊÕãíã äåÇíí ÈÇ ÚŞá æ Êæ˜á ÔãÇÓÊ."
    }

@app.post("/api/raml")
async def api_raml(req: RamlRequest):
    """ãÍÇÓÈå Ñãá æ ÊİÓíÑ AI"""
    # ÊæáíÏ ? Ô˜á ãÇÏÑ Èå ÕæÑÊ ÊÕÇÏİí (ÏÑ äÓÎå æÇŞÚí¡ ˜ÇÑÈÑ äŞØååÇ Ñæ ãí˜Ôå)
    mothers = []
    for _ in range(4):
        shape = [random.randint(0, 1) for _ in range(4)]
        mothers.append(shape)
    
    result = raml_analysis(mothers)
    
    prompt = f"""
    ˜ÇÑÈÑ ÈÇ äÇã "{req.name}" ÓæÇá ÒíÑ ÑÇ ÑÓíÏå ÇÓÊ:
    "{req.question}"
    
    äÊÇíÌ ãÍÇÓÈÇÊ Ñãá:
    ÎÇäå ? (ÎæÏ): {result[1]['shape']} - {result[1]['meaning']}
    ÎÇäå ? (ãÇá): {result[2]['shape']} - {result[2]['meaning']}
    ÎÇäå ? (ÔÑÇ˜Ê): {result[7]['shape']} - {result[7]['meaning']}
    ÎÇäå ?? (ÔÛá): {result[10]['shape']} - {result[10]['meaning']}
    ÎÇäå ?? (ÏÔãäÇä): {result[12]['shape']} - {result[12]['meaning']}
    ŞÇÖí (Í˜ã äåÇíí): {result[15]['shape']} - {result[15]['meaning']}
    
    áØİÇğ ÈÑ ÇÓÇÓ Çíä ÏÇÏååÇ¡ í˜ ÊİÓíÑ ÌÇãÚ æ ÑÇå˜ÇÑ Úãáí ÇÑÇÆå ÈÏå.
    """
    
    ai_text = await get_ai_interpretation(prompt)
    
    return {
        "method": "raml",
        "houses": result,
        "interpretation": ai_text,
        "disclaimer": "Çíä ÊÍáíá ÕÑİÇğ ÈÑÇí ÓÑÑãí æ ÂãæÒÔ ÇÓÊ. ÊÕãíã äåÇíí ÈÇ ÚŞá æ Êæ˜á ÔãÇÓÊ."
    }

ãÏíÑ ÍãÊÇ, [27/09/2026 08:36 È.Ù]
@app.post("/api/combined")
async def api_combined(req: AIRequest):
    """ÊÑ˜íÈ ÌİÑ æ Ñãá ÈÇ ÊİÓíÑ AI"""
    jafr_result = full_jafr(req.name, req.mother_name, req.question)
    
    mothers = [[random.randint(0, 1) for _ in range(4)] for _ in range(4)]
    raml_result = raml_analysis(mothers)
    
    prompt = f"""
    ˜ÇÑÈÑ "{req.name}" ÓæÇá ÒíÑ ÑÇ ÑÓíÏå ÇÓÊ:
    "{req.question}"
    
    --- äÊÇíÌ ÌİÑ ---
    ãäÒá ŞãÑí: {jafr_result['akbar']['name']} - {jafr_result['akbar']['meaning']}
    ÈÑÌ: {jafr_result['asghar']['name']} - {jafr_result['asghar']['meaning']}
    ÎáØ: {jafr_result['akhlat']['khilt']} ({jafr_result['akhlat']['tab']})
    
    --- äÊÇíÌ Ñãá ---
    ŞÇÖí (Í˜ã äåÇíí): {raml_result[15]['shape']} - {raml_result[15]['meaning']}
    ÎÇäå ? (ÔÑÇ˜Ê): {raml_result[7]['shape']} - {raml_result[7]['meaning']}
    ÎÇäå ?? (ÔÛá): {raml_result[10]['shape']} - {raml_result[10]['meaning']}
    
    áØİÇğ Çíä Ïæ ÑæÔ ÑÇ ÊáİíŞ ˜ä æ í˜ ÊİÓíÑ æÇÍÏ¡ ÌÇãÚ æ ÑÇåÔÇ ÇÑÇÆå ÈÏå.
    """
    
    ai_text = await get_ai_interpretation(prompt)
    
    return {
        "method": "combined",
        "jafr": jafr_result,
        "raml": raml_result,
        "interpretation": ai_text,
        "disclaimer": "Çíä ÊÍáíá ÕÑİÇğ ÈÑÇí ÓÑÑãí æ ÂãæÒÔ ÇÓÊ. ÊÕãíã äåÇíí ÈÇ ÚŞá æ Êæ˜á ÔãÇÓÊ."
    }

@app.get("/")
def root():
    return {"message": "Jafr & Raml AI API is running", "status": "ok"}