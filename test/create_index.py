from elasticsearch import Elasticsearch
import os
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

# 인덱스 삭제 (이미 있으면 삭제)
if es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME)

# 인덱스 생성 및 매핑 정의
mapping = {
    "mappings": {
        "properties": {
            "doc_id": {"type": "keyword"},
            "title": {"type": "text"},
            "chunk_index": {"type": "integer"},
            "content": {"type": "text"},
            "embedding": {
                "type": "dense_vector",
                "dims": 1024    # e5-large 임베딩 차원 수 확인 필요 (보통 768 또는 512)
            },
            "source": {"type": "keyword"}
        }
    }
}

es.indices.create(index=INDEX_NAME, body=mapping)

print(f"Elasticsearch index '{INDEX_NAME}' created with dense_vector mapping.")
