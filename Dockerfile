FROM python:3.6
RUN pip install pipenv
WORKDIR /app
ADD . .
RUN pipenv install
ENTRYPOINT ["pipenv", "run", "python", "codesort.py"]
CMD ["/repo"]
