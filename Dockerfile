# Use official Python image as base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files (avoiding unnecessary files like .git, __pycache__)
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Use Gunicorn with Uvicorn for better performance in production
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]
