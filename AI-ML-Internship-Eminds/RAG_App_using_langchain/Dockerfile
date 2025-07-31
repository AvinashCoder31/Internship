# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy dependency file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy rest of the app
COPY . .

# Expose port (optional if using Flask)
EXPOSE 5000

# Set the entrypoint to run the app
CMD ["python", "main.py"]

# Step 1: Build the Docker image
# docker build -t rag-langchain-app .

# Step 2: Run the Docker container
# docker run -it --env-file .env rag-langchain-app


