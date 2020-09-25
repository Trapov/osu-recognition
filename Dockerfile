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

CMD [ "uvicorn", "runnable_packages.rest.api:app" ,"-h", "0.0.0.0" , "-port" "80", "-w", "4" ]