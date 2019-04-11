FROM debian:stretch

RUN echo "Installing graph-tool" \
    && echo "deb http://downloads.skewed.de/apt/stretch stretch main" >> /etc/apt/sources.list \
    && echo "deb-src http://downloads.skewed.de/apt/stretch stretch main" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install \
            git
            python3
            python3-pip
            python3-graph-tool
         -y --allow-unauthenticated \
    && pip3 install gitpython

WORKDIR /app
ADD codesort.py .

ENTRYPOINT ["python3", "codesort.py"]
