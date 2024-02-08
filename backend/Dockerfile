FROM python:3.9-slim

WORKDIR /app

COPY app.py /app/
COPY Dockerfile /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 8501

CMD [ "python", "app.py" ]