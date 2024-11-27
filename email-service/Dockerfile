# Use an official Python runtime as a parent image
FROM python:3.12.7-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the wait-for-it.sh script to the container and make it executable
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Expose port 8000 to the outside world
EXPOSE 8083

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Command to run the FastAPI app with Uvicorn, waiting for Kafka to be ready
ENTRYPOINT ["/app/wait-for-it.sh", "kafka:9092", "--", "python", "main.py"]
