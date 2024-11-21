# Start with a base Python image
FROM python:3.11-slim

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port that Flask will run on
EXPOSE 5050

# Define the command to run the Flask application
CMD ["python3", "run.py"]
