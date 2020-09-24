FROM dmitriyafonin/osu-recognition-base

ARG COMMIT_HASH
ARG VERSION

ENV COMMIT_HASH=${COMMIT_HASH}
ENV VERSION=${VERSION}

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "run-rest-api.py"]