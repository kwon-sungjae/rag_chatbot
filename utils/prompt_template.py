# 프롬프트 템플릿 모듈

def build_prompt(question: str, context: str) -> str:
    prompt = f"""
    다음은 기업 내부 문서에서 검색된 정보입니다. 이 정보를 바탕으로 사용자의 질문에 친절하고 명확하게 답변해주세요.
    [문서 내용]
    {context}
    [질문]
    {question}
    [답변]
    """
    return prompt

def corpus_gen_prompt(seed_text: str = "기업용 데이터 생성") -> str:
    return (
        f"{seed_text} 요청입니다.\n"
        "아래 조건에 따라 가상의 기업 내부 문서를 생성하세요.\n\n"
        "[조건]\n"
        "- 한국의 중견 기업 설정\n"
        "- 'company', 'title', 'content' 3개의 키를 가진 JSON 형식으로 출력\n"
        "- content는 500자 이상, 보고서 형식으로 작성\n\n"
        "출력 예시:\n"
        '{\n  "company": "그린에너지솔루션 주식회사",\n  "title": "2025년 하반기 신재생에너지 전략 보고서",\n  "content": "[개요]\\n2025년 하반기를 맞아..." \n}\n\n'
        "이제 JSON 형식으로 출력하세요."
    )
