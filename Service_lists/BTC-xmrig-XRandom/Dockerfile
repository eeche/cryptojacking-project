# XMRig Dockerfile

# 기본 이미지를 최신 Ubuntu LTS 버전으로 지정합니다.
FROM ubuntu:20.04

# 환경 변수를 설정하여 비대화형 모드로 만듭니다.
ENV DEBIAN_FRONTEND=noninteractive

# 패키지 업데이트 및 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y \
    wget \
    build-essential \
    cmake \
    libhwloc-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# XMRig 소스코드 다운로드 및 빌드
RUN wget https://github.com/xmrig/xmrig/releases/download/v6.18.0/xmrig-6.18.0-linux-x64.tar.gz && \
    tar -xvf xmrig-6.18.0-linux-x64.tar.gz && \
    mv xmrig-6.18.0 /xmrig && \
    rm xmrig-6.18.0-linux-x64.tar.gz

# XMRig 설정 파일을 컨테이너에 복사
COPY config.json /xmrig/config.json

# XMRig를 실행
CMD ["/xmrig/xmrig", "--config", "/xmrig/config.json"]

