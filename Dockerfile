#FROM python:3.8-slim
FROM python:3.10-slim
ENV PYTHONNUNBUFFERED 1

RUN apt-get update
#RUN apt-get install sudo
RUN apt-get install -y default-jre
RUN apt-get install -y redis-server
#sudo apt install tesseract-ocr poppler-utils
#RUN apt-get install -y tesseract-ocr
#RUN apt-get install -y poppler-utils
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-eng \
        poppler-utils && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install uvicorn[standard]
COPY . /app/
