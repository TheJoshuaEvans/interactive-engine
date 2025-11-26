# Dockerfile by @portalsoup - Thank you!
FROM python:3.12-slim

ENV PYTHONPATH=/app/src

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m unittest discover -s src -p "test*.py"

CMD ["python", "wizard_emergency.py"]
