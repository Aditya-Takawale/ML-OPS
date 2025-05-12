# Use a lightweight and specific Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only essential files first to improve caching
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Activate the virtual environment and train the model
RUN . venv/bin/activate && python pipeline/training_pipeline.py

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the application inside the virtual environment
CMD ["/bin/sh", "-c", ". venv/bin/activate && python application.py"]
