# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the PYTHONPATH so the app can find the 'src' folder
ENV PYTHONPATH=/app/src

# Expose the port the API runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.dynacache.api.main_api:app", "--host", "0.0.0.0", "--port", "8000"]