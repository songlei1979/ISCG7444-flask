# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose port Flask will run on
EXPOSE 5000

# Set environment variable (optional)
ENV FLASK_APP=app.py

# Start the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
