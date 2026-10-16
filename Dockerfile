FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1
ENV DB_URL=sqlite:////app/data/family_bot.db
ENV PORT=5000

CMD ["python", "bot.py"]
