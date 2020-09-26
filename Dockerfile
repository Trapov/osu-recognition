FROM dmitriyafonin/osu-recognition-base

ARG COMMIT_HASH
ARG VERSION
ARG PORT=80
ARG WORKERS=4

ENV COMMIT_HASH=${COMMIT_HASH}
ENV VERSION=${VERSION}
ENV WORKERS=${WORKERS}
ENV PORT=${PORT}

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN chmod +x ./start.sh

CMD uvicorn runnable_packages.rest.api:app --host=0.0.0.0 --port=${PORT} --workers=${WORKERS}