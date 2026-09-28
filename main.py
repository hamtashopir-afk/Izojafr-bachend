from fastapi import FastAPI
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
from jafr_engine import full_jafr
from raml_engine import raml_analysis
import random

app = FastAPI(title="Jafr Raml AI")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY is not set.")

client = AsyncOpenAI(
    base_url="https://api.deepseek.com",
    api_key=DEEPSEEK_API_KEY,
)

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
    method: str

async def get_ai_interpretation(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert interpreter of traditional Jafr and Raml sciences. Based on the calculation results, provide a comprehensive, empathetic, and practical interpretation in Persian. Your tone should be calming and guiding. Never claim certainty, and always emphasize that this analysis is symbolic."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/api/jafr")
async def api_jafr(req: JafrRequest):
    result = full_jafr(req.name, req.mother_name, req.question)
    prompt = f"""
    User with name {req.name} and mother name {req.mother_name} asked: {req.question}
    Jafr results:
    Total number: {result['total']}
    Jafr Akbar: {result['akbar']['name']} - {result['akbar']['meaning']}
    Jafr Asghar: {result['asghar']['name']} ({result['asghar']['element']}) - {result['asghar']['meaning']}
    Akhlat: {result['akhlat']['khilt']} ({result['akhlat']['tab']})
    Direction: {result['akhlat']['direction']}
    Season: {result['akhlat']['season']}
    Provide a comprehensive interpretation and practical solution in Persian.
    """
    ai_text = await get_ai_interpretation(prompt)
    return {
        "method": "jafr",
        "numbers": result,
        "interpretation": ai_text,
        "disclaimer": "This analysis is for entertainment and educational purposes only."
    }

@app.post("/api/raml")
async def api_raml(req: RamlRequest):
    mothers = []
    for _ in range(4):
        shape = [random.randint(0, 1) for _ in range(4)]
        mothers.append(shape)
    result = raml_analysis(mothers)
    prompt = f"""
    User with name {req.name} asked: {req.question}
    Raml results:
    House 1 (Self): {result[1]['shape']} - {result[1]['meaning']}
    House 2 (Money): {result[2]['shape']} - {result[2]['meaning']}
    House 7 (Partnership): {result[7]['shape']} - {result[7]['meaning']}
    House 10 (Career): {result[10]['shape']} - {result[10]['meaning']}
    House 12 (Enemies): {result[12]['shape']} - {result[12]['meaning']}
    Judge (Final verdict): {result[15]['shape']} - {result[15]['meaning']}
    Provide a comprehensive interpretation and practical solution in Persian.
    """
    ai_text = await get_ai_interpretation(prompt)
    return {
        "method": "raml",
        "houses": result,
        "interpretation": ai_text,
        "disclaimer": "This analysis is for entertainment and educational purposes only."
    }

@app.post("/api/combined")
async def api_combined(req: AIRequest):
    jafr_result = full_jafr(req.name, req.mother_name, req.question)
    mothers = [[random.randint(0, 1) for _ in range(4)] for _ in range(4)]
    raml_result = raml_analysis(mothers)

prompt = f"""
    User {req.name} asked: {req.question}
    Jafr Akbar: {jafr_result['akbar']['name']} - {jafr_result['akbar']['meaning']}
    Jafr Asghar: {jafr_result['asghar']['name']} - {jafr_result['asghar']['meaning']}
    Akhlat: {jafr_result['akhlat']['khilt']}
    Raml Judge: {raml_result[15]['shape']} - {raml_result[15]['meaning']}
    Raml House 7: {raml_result[7]['shape']} - {raml_result[7]['meaning']}
    Raml House 10: {raml_result[10]['shape']} - {raml_result[10]['meaning']}
    Combine these and provide a unified interpretation in Persian.
    """
    ai_text = await get_ai_interpretation(prompt)
    return {
        "method": "combined",
        "jafr": jafr_result,
        "raml": raml_result,
        "interpretation": ai_text,
        "disclaimer": "This analysis is for entertainment and educational purposes only."
    }

@app.get("/")
def root():
    return {"message": "Jafr Raml AI API is running", "status": "ok"}
