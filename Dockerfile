FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
# Run from project root so KEYS_PATH and DATABASE_URL (data/, keys/) resolve at root
# In production, set env KEYS_PATH=/keys, DATABASE_URL=sqlite:////data/app.db and mount volumes
CMD ["python", "-m", "app.main"]
