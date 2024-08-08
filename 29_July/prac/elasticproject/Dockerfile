# Dockerfile
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install  -r requirements.txt

# Copy the project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Start the application
CMD ["gunicorn", "elasticproject.wsgi:application", "--bind", "0.0.0.0:8000"]
