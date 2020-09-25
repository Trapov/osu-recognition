FROM dmitriyafonin/osu-recognition-base

ARG COMMIT_HASH
ARG VERSION
ARG PORT=80

ENV COMMIT_HASH=${COMMIT_HASH}
ENV VERSION=${VERSION}
ENV PORT=${PORT}

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "./start.sh" ]