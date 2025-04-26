# From https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/
# =======================================================================
FROM python:3.12-slim

WORKDIR /ReceiptiPy

# COPY 
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

# running our container
CMD ["gunicorn", "--bind" , "0.0.0.0:5000", "wsgi:app"]
