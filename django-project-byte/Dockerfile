FROM python:3.9-slim

# 기본 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# trace-cmd 설치를 위한 패키지 업데이트 및 설치
RUN apt-get update && apt-get install -y trace-cmd

# 소스 코드 복사
COPY . .

# 컨테이너가 실행될 때 실행할 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
