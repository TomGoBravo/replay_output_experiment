FROM python:3.7-slim

RUN echo 'deb http://http.debian.net/debian jessie-backports main' >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends apt-utils

ENV PIP_FORMAT=legacy
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get install -y netcat && apt-get autoremove -y

# Create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

WORKDIR /replay_output_experiment/

COPY . /replay_output_experiment

RUN pip3 install -e .

ENTRYPOINT ["./run.sh"]

