# From https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/
# =======================================================================
FROM python:3.12-slim

WORKDIR /ReceiptiPy

# COPY 
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .

# running our container
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
