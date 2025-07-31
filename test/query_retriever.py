import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elasticsearch import Elasticsearch
from retriever.elastic_search import search_documents
from embedder.chunk_embedder import embed_query

from dotenv import load_dotenv

load_dotenv()

es = Elasticsearch(
    os.getenv("ELASTICSEARCH_HOST"),
    basic_auth=(
        os.getenv("ELASTICSEARCH_USERNAME"),
        os.getenv("ELASTICSEARCH_PASSWORD")
    ),
    verify_certs=False
)

INDEX_NAME = "documents_index"

def search_similar_documents(question: str, k=3):
    # 1. 질문 임베딩 생성
    query_vector = embed_query(question)

    # 2. Elasticsearch에서 벡터 유사도 검색
    results = search_documents(query_vector, k=k)
    return results

if __name__ == "__main__":
    question = "코리아테크 주식회사의 2023년 상반기 동안 매출은?"
    search_results = search_similar_documents(question, k=3)
    print("검색 결과:")
    for idx, doc in enumerate(search_results, 1):
        print(f"{idx}. {doc}\n")
