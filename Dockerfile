# build networkit
FROM python:3.6-stretch as builder
RUN apt-get update && apt-get install -y \
        cmake \
        build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install \
        gitpython==2.1.11 \
        networkit==5.0

# codesort image
FROM python:3.6-stretch
COPY --from=builder /usr/local/lib/python3.6 /usr/local/lib/python3.6
WORKDIR /app
COPY codesort.py .
ENTRYPOINT ["/usr/local/bin/python3.6", "codesort.py", "/repo"]
