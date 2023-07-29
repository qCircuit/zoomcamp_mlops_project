FROM python:3.9-slim

RUN pip install -U pip

COPY ["requirements.txt", "./"]

RUN pip install -r requirements.txt

WORKDIR /app

COPY ["predict.py", "model.joblib", "./"]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app"]
