FROM gcr.io/distroless/python3-debian10

COPY requirements.txt /run/requirements.txt

RUN cd requirements.txt && pip install -r requirements.txt

COPY docker-historian.py /run/docker-historian.py

WORKDIR /run/

ENTRYPOINT ["python","docker-historian.py"]
