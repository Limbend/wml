FROM python:3.9-slim
LABEL version="0.1"

WORKDIR /app
ADD ./requirements.txt .
RUN pip install -r ./requirements.txt

ADD ./ ./