import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator.gpt_generator import generate_internal_corpus_json  # 앞서 만든 함수
from db.mysql_connector import insert_document

def generate_and_store_document():
    data = generate_internal_corpus_json()

    if "error" in data:
        print("문서 생성 실패:", data["raw"])
        return None

    company = data["company"]
    title = data["title"]
    content = data["content"]

    # source 필드에 회사명 넣는 것도 방법
    source = company

    doc_id = insert_document(title=title, content=content, source=source, is_embedded=0)
    print(f"✅ 문서 저장 완료, id: {doc_id}")

    return doc_id

if __name__ == "__main__":
    for i in range(5):
        generate_and_store_document()