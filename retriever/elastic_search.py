# Elasticsearch를 통한 벡터 기반 문서 검색 모듈
import os
from elasticsearch import Elasticsearch
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

INDEX_NAME = "documents_index"  # 사전에 정의된 문서 인덱스 이름

def search_documents(query_vector, k=3):
    response = es.search(
        index=INDEX_NAME,
        size=k,
        query={
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    )

    documents = []
    for hit in response['hits']['hits']:
        documents.append(hit['_source']['content'])

    return documents
