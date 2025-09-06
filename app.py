import streamlit as st
from retriever.elastic_search import search_documents, es, INDEX_NAME
from generator.gpt_generator import generate_answer
from embedder.chunk_embedder import embed_query
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="RAG 기업 챗봇", layout="wide")

st.title("💬 RAG 기반 기업 챗봇 시스템")

# 탭 구성
tab1, tab2 = st.tabs(["🤖 챗봇", "📊 Elasticsearch 대시보드"])

# ==========================
# 1️⃣ RAG 챗봇 탭
# ==========================
with tab1:
    question = st.text_input("질문을 입력하세요:")

    if st.button("질문하기", key="ask_btn") and question:
        # ==========================
        # 1️⃣ 입력 질문
        # ==========================
        st.markdown("### 📝 입력 질문")
        st.info(question)

        with st.spinner("질문 임베딩 생성 중..."):
            # 2. 질문 임베딩 생성
            question_vec = embed_query(question)

        st.markdown("### 🔢 질문 임베딩 (샘플)")
        st.code(str(question_vec[:10]) + " ...")  # 앞부분 10개만 출력

        with st.spinner("문서 검색 중..."):
            # 3. 유사 문서 검색
            docs = search_documents(question_vec, k=3)

        if docs:
            # ==========================
            # 4️⃣ 검색된 문서 (Top-k)
            # ==========================
            st.markdown("### 📄 검색된 문서 (Top-3)")
            for i, doc in enumerate(docs, 1):
                st.write(f"**문서 {i}**")
                st.write("내용:", doc[:300] + "...")
                st.divider()

            # ==========================
            # 5️⃣ LLM 입력 프롬프트
            # ==========================
            with st.spinner("응답 생성 중..."):
                # generate_answer 함수는 그대로 사용
                answer = generate_answer(question, docs)

            # 프롬프트 출력 부분은 제거하거나 주석 처리
            # st.markdown("### 🧩 LLM 입력 프롬프트")
            # st.code(prompt)

            # ==========================
            # 6️⃣ 최종 답변
            # ==========================
            st.markdown("### 💡 최종 답변")
            st.success(answer)

        else:
            st.warning("관련 문서를 찾지 못했습니다.")

# ==========================
# 2️⃣ Elasticsearch 대시보드 탭
# ==========================
with tab2:
    st.subheader("📊 Elasticsearch 대시보드")

    # 탭2를 다시 세분화 (매핑 / 문서 확인)
    dash_tab1, dash_tab2 = st.tabs(["🗂 인덱스 매핑", "📄 문서 데이터"])

    # ==========================
    # 1️⃣ 인덱스 매핑 확인
    # ==========================
    with dash_tab1:
        try:
            mapping = es.indices.get_mapping(index=INDEX_NAME)
            st.json(mapping[INDEX_NAME]["mappings"]["properties"])  # properties 부분만 출력
        except Exception as e:
            st.error(f"매핑 조회 중 오류 발생: {e}")

    # ==========================
    # 2️⃣ 문서 데이터 확인
    # ==========================
    with dash_tab2:
        size = st.slider("표시할 문서 개수", min_value=1, max_value=20, value=5)
        try:
            docs = es.search(index=INDEX_NAME, size=size, query={"match_all": {}})
            hits = docs["hits"]["hits"]

            if hits:
                for i, hit in enumerate(hits, 1):
                    st.markdown(f"### 문서 {i}")
                    st.write("**doc_id:**", hit["_source"].get("doc_id", "없음"))
                    st.write("**title:**", hit["_source"].get("title", "없음"))
                    st.write("**source:**", hit["_source"].get("source", "없음"))
                    st.write("**chunk_index:**", hit["_source"].get("chunk_index", "없음"))
                    st.write("**content:**", hit["_source"].get("content", "")[:500] + "...")
                    st.divider()
            else:
                st.info("현재 인덱스에 문서가 없습니다.")
        except Exception as e:
            st.error(f"문서 조회 중 오류 발생: {e}")