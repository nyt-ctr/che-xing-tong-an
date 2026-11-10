FROM python:3.11-slim

WORKDIR /app

# MediaPipe/OpenCV need these system libraries
RUN apt-get update && apt-get install -y --no-install-recommends     libgl1     libglib2.0-0     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# DevCloud only routes traffic to port 8080
EXPOSE 8080

# Bind 0.0.0.0:8080, 1 worker + 4 threads for frame analysis
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "--timeout", "300", "web_app:app"]
