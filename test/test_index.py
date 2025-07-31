import sys
import os
import uuid
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elasticsearch import Elasticsearch
from embedder.chunk_embedder import chunk_text, embed_chunks
from db.mysql_connector import fetch_unembedded_documents, mark_document_as_embedded

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

# 문서 임베딩 및 색인 처리
def embed_and_index_documents():
    documents = fetch_unembedded_documents()

    for doc in tqdm(documents, desc="Embedding & Indexing"):
        doc_id = doc["id"]
        title = doc["title"]
        content = doc["content"]
        source = doc["source"]

        # 1. 텍스트 청킹
        chunks, embeddings = embed_chunks(content, chunk_size=512, stride=12)

        # 3. 각 청크를 Elasticsearch에 색인
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            es.index(
                index=INDEX_NAME,
                id=str(uuid.uuid4()),  # 색인 고유 ID
                document={
                    "doc_id": doc_id,
                    "title": title,
                    "chunk_index": i,
                    "content": chunk,
                    "embedding": embedding,
                    "source": source
                }
            )

        # 4. 색인 완료 표시
        mark_document_as_embedded(doc_id)


if __name__ == "__main__":
    embed_and_index_documents()