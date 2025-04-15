FROM python:3.12-slim

# system dependencies. What we want machine to do when it starts
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /spotify-haiku-api

COPY . .

# stay safe by upgrading to latest pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# running our container
CMD ["python3", "app.py"]
