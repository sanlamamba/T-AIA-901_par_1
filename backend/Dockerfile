FROM python:3.11

RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./API/setup_vosk.sh

RUN ./API/setup_vosk.sh

EXPOSE 5000

CMD ["python", "manage.py"]
