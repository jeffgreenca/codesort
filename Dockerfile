FROM python:3.6-stretch
RUN apt-get update && apt-get install -y \
        cmake \
        build-essential \
        python3-tk \
    && rm -rf /var/lib/apt/lists/*
RUN pip install \
        gitpython==2.1.11 \
        networkit==5.0
WORKDIR /app
COPY *.py .
ENTRYPOINT ["python"]
CMD ["validate-nk-install.py"]
