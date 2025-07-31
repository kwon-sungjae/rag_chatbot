# GPT API를 활용한 응답 생성 모듈
from openai import OpenAI
import os
from dotenv import load_dotenv
from utils.prompt_template import build_prompt, corpus_gen_prompt
import json


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question: str, documents: list) -> str:
    context = "\n\n".join(documents)

    prompt = build_prompt(question, context)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 또는 "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "당신은 친절한 기업 정보 안내 챗봇입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=512
    )

    return response.choices[0].message.content.strip()

def generate_internal_corpus_json(seed_text: str = "기업용 데이터 생성") -> dict:
    prompt = corpus_gen_prompt(seed_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 기업 내부 문서를 생성하는 AI입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1024
    )

    raw_text = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        result = {"error": "JSON 파싱 실패", "raw": raw_text}

    return result