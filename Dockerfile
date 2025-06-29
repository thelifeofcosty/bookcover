# Use the official Apify Python actor base image
FROM apify/actor-python:3.9

# Copy everything into the container
COPY . /usr/src/app
WORKDIR /usr/src/app

# Install dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Run your Python entrypoint
CMD ["python3", "main.py"]
