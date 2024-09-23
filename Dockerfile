FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY cli.py database.py models.py utils.py ./

CMD ["bash", "-c", "python cli.py; exec bash"]