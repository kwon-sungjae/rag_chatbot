# MySQL 연결 유틸리티
import os
import mysql.connector
from dotenv import load_dotenv
import uuid

load_dotenv()

# 환경 세팅
def get_connection():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=os.getenv("MYSQL_PORT"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
    return conn

# 생성 문서(Data) 저장
def insert_document(title: str, content: str, source: str = None, is_embedded: int = 0):
    conn = get_connection()
    cursor = conn.cursor()

    doc_id = str(uuid.uuid4())  # UUID 생성
    sql = """
    INSERT INTO documents (id, title, content, source, is_embedded)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (doc_id, title, content, source, is_embedded))
    conn.commit()

    cursor.close()
    conn.close()

    return doc_id

# 문서 임베딩 여부 확인
def fetch_unembedded_documents():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM documents
    WHERE is_embedded = 0
    """
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

# 임베딩 완료 여부 업데이트
def mark_document_as_embedded(doc_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    UPDATE documents
    SET is_embedded = 1
    WHERE id = %s
    """
    cursor.execute(sql, (doc_id,))
    conn.commit()

    cursor.close()
    conn.close()