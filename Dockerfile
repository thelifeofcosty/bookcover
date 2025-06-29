# Use Apify’s Python base image
FROM apify/python:3.9

# Copy all your code into the container
COPY . /usr/src/app

# Switch to that directory
WORKDIR /usr/src/app

# Install your Python deps
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Run your Python main script
CMD ["python3", "main.py"]
