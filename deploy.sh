#!/bin/bash
# ────────────────────────────────────────────
# deploy.sh  —  로컬에서 실행하면 push + EC2 배포까지 자동
# 사용법: bash deploy.sh "커밋 메시지"
# ────────────────────────────────────────────

# ── 설정값 (본인 환경에 맞게 수정) ──
EC2_IP="your_ec2_ip"              # EC2 퍼블릭 IP
EC2_USER="ubuntu"
PEM_PATH="./rag-key.pem"          # 로컬 pem 파일 경로
REMOTE_DIR="~/rag_chatbot"

COMMIT_MSG=${1:-"update"}         # 인자 없으면 "update"

echo "▶ [1/3] Git push..."
git add -u                        # 추적 중인 파일만 add (신규 파일은 수동 add)
git commit -m "$COMMIT_MSG"
git push origin main

echo "▶ [2/3] EC2 pull & 재시작..."
ssh -i "$PEM_PATH" "$EC2_USER@$EC2_IP" << 'REMOTE'
  cd ~/rag_chatbot
  git pull origin main
  source venv/bin/activate
  pip install -r requirements_cpu.txt -q   # 새 패키지 자동 설치

  # 기존 streamlit 종료 후 재시작
  pkill -f "streamlit run" 2>/dev/null || true
  sleep 1
  nohup streamlit run app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    > ~/streamlit.log 2>&1 &
  echo "Streamlit PID: $!"
REMOTE

echo "▶ [3/3] 완료! http://$EC2_IP:8501 에서 확인하세요."
