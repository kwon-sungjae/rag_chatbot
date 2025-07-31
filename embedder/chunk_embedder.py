import os
from openai import OpenAI
from dotenv import load_dotenv

from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
import numpy as np

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# e5-large 임베딩 모델 로딩 
MODEL_NAME = "intfloat/multilingual-e5-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
embedding_model = SentenceTransformer(MODEL_NAME)

# 질문 임베딩(no chunk)
def embed_query(text: str):
    """
    질문 텍스트를 바로 임베딩 (청크 불필요)
    """
    embedding = embedding_model.encode([text])  # 리스트로 감싸서 batch 처리
    return embedding[0].tolist()

# 텍스트 청크
def chunk_text(text: str, chunk_size: int = 512, stride: int = 12) -> list[str]:
    """
    텍스트를 토큰 기준으로 512 토큰씩 자르고, 12토큰 겹치게(overlap) 청킹
    """
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
        if end >= len(tokens):
            break
        start += chunk_size - stride

    return chunks

# 청킹된 텍스트 임베딩
def embed_chunks(text: str, chunk_size: int = 512, stride: int = 12):
    chunks = chunk_text(text, chunk_size, stride)
    embeddings = embedding_model.encode(chunks)
    return chunks, embeddings.tolist()





# gpt_api 임베딩 모델 사용하지 않을 것임으로 주석 처리
# def get_embedding(text, model="text-embedding-3-small"):
#     response = client.embeddings.create(
#         input=text,
#         model=model
#     )
#     return response.data[0].embedding