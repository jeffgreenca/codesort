# build networkit
FROM python:3.6-stretch as builder
RUN apt-get update && apt-get install -y \
        cmake \
        build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install \
        gitpython==2.1.11 \
        networkit==5.0
RUN pip install virtualenv && virtualenv .venv \
    && cp -r /usr/local/lib/python3.6/site-packages/* .venv/lib/python3.6/site-packages/

# codesort image
FROM python:3.6-stretch
COPY --from=builder /.venv .venv
WORKDIR /app
COPY codesort.py .
ENTRYPOINT ["/.venv/bin/python", "codesort.py", "/repo"]
