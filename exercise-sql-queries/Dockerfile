FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY populate_db.py /app
COPY add_records.py /app
RUN mkdir /app/data
COPY ./data/person.tsv /app/data/person.tsv
COPY ./data/drug.tsv /app/data/drug.tsv
COPY ./data/diagnosis.tsv /app/data/diagnosis.tsv
COPY ./data/prescription.tsv /app/data/prescription.tsv
COPY ./data/visit.tsv /app/data/visit.tsv


ENV DB_HOST=${DB_HOST}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_NAME=${DB_NAME}

ENTRYPOINT [ "python" ]
CMD [ "populate_db.py" ]
