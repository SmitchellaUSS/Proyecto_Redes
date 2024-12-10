
FROM python:3.10-slim


RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir psycopg2-binary


EXPOSE 5000 5001


CMD ["python", "server.py"]
