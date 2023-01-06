FROM python:3.8-slim-buster

ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# copy whole project to your docker home directory. 
COPY . $DockerHOME  
# run this command to install all dependencies 
RUN pip install poetry 
RUN poetry install --no-dev
RUN poetry run python manage.py makemigrations
RUN poetry run python manage.py migrate

# port where the Django app runs  
EXPOSE 8000  
# start server  
# CMD python manage.py runserver 