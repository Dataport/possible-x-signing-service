FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=server.py
ENV FLASK_ENV=production

# Run flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
