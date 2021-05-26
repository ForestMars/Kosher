FROM python:3.8.5-slim

COPY app.py /app/
COPY build/predict/requirements.txt /app/
COPY models/hackles/hackles.pkl /app/models/hackles/
COPY build/src/trans.py /app/build/src/
WORKDIR /app

RUN apt-get -y update
RUN apt-get install -y python3-pip
RUN python3 -m pip install -r requirements.txt

ARG FLASK_RUN_PORT
ENV FLASK_RUN_PORT $FLASK_RUN_PORT

CMD ["python3", "./app.py", "port=${FLASK_RUN_PORT}"]


# As of 18.03.0-ce, Docker now alllows COPY file outside the build context:
# https://github.com/docker/cli/pull/886
~
