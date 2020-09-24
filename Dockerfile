  
# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition

FROM python:3.8-slim-stretch

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python" "run-rest-api.py"]