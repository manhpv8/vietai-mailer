# cat Dockerfile
FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["bash", "workflows/start.sh"]

EXPOSE 8000