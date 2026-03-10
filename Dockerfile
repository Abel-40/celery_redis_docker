FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY ./requirement.txt .

RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirement.txt

COPY . .

EXPOSE 8000
