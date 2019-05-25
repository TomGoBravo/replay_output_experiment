FROM python:3.7-slim
    
RUN echo 'deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main' >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends apt-utils dumb-init

ENV PIP_FORMAT=legacy
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get install -y netcat && apt-get autoremove -y

# Create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

WORKDIR /repo_root

# Copy all of the directory tree containing Dockerfile to /repo_root in the image. This
# copy is used for the pip3 install below. At runtime the live data on the host is mounted
# at the same directory in the container (see `volumes` in `docker-compose.yaml`). The mount
# hides the copy in the image and lets the container access the latest code on the host.
COPY . /repo_root

RUN pip3 install -r /repo_root/requirements.txt

# https://github.com/Yelp/dumb-init#using-a-shell-for-pre-start-hooks
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/repo_root/run.sh"]
