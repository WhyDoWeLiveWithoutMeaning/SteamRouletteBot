FROM python:3.12-slim

# Set the working directory
WORKDIR /app

COPY . /app
RUN pip3 install -r requirements.txt

# Run the application
CMD ["python3", "main.py"]