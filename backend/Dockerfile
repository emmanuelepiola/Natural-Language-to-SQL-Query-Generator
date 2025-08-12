FROM python:3.11-slim

WORKDIR /app

COPY ./backend/requirements.txt .

RUN apt-get update
RUN apt-get install -y libmariadb-dev
RUN apt-get install -y build-essential
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend/src/ src/

EXPOSE 8003

CMD ["uvicorn", "src.backend.backend:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]

