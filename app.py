import streamlit as st
from retriever.elastic_search import search_documents
from generator.gpt_generator import generate_answer
from embedder.chunk_embedder import embed_query  # E5 임베딩 임포트 (기존 get_embedding 대체)
from dotenv import load_dotenv

load_dotenv()

st.title("💬 RAG 기반 기업 챗봇")

question = st.text_input("질문을 입력하세요:")

if st.button("질문하기") and question:
    with st.spinner("검색 중..."):
        # 1. 질문 임베딩 생성
        question_vec = embed_query(question)

        # 2. 유사 문서 검색 (k=3으로 설정 가능)
        docs = search_documents(question_vec, k=3)

    if docs:
        with st.spinner("답변 생성 중..."):
            # 3. 검색 문서 + 질문으로 GPT 답변 생성
            answer = generate_answer(question, docs)
        st.markdown("### 💡 답변:")
        st.write(answer)
    else:
        st.write("관련 문서를 찾지 못했습니다.")