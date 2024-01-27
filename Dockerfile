FROM python:3.11

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0"]
