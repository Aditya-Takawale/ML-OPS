# Use a lightweight Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (for LightGBM)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install dependencies (NO venv)
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Train model (optional — only if needed at container build time)
RUN python pipeline/training_pipeline.py

# Expose Cloud Run default port
EXPOSE 8080

# Run the app
CMD ["python", "application.py"]
