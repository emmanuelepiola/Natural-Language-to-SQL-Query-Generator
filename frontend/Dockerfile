FROM python:3.11-slim

WORKDIR /app

COPY ./frontend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./frontend/src/ src/
COPY ./frontend/templates/ templates/

EXPOSE 8000

CMD ["uvicorn", "src.frontend.frontend:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]