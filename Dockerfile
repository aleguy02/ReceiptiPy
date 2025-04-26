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
CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]
