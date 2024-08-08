# Use the official Python image as a base image
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
# Set the working directory in the container
WORKDIR /app

# Install gcc and other necessary packages
RUN apt-get update && apt-get install -y gcc

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Django app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
