# Use the official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any required dependencies (if applicable)
RUN pip install -r requirements.txt

RUN apt-get update && \
     apt-get install -y libgl1-mesa-glx libglib2.0-0


# Expose the port on which your Flask app runs
EXPOSE 5000

# Run your Flask app
CMD ["python", "app.py"]
