FROM dmitriyafonin/osu-recognition-base

ARG COMMIT_HASH
ARG VERSION
ARG PORT=80

ENV COMMIT_HASH=${COMMIT_HASH}
ENV VERSION=${VERSION}

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "uvicorn", "runnable_packages.rest.api:app" ,"--host=0.0.0.0" , "--port=${PORT}", "--workers=4" ]