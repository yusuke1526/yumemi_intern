FROM python:3.9-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 80
ENTRYPOINT ["python3","/code/manage.py","migrate","&&","python3","/code/manage.py","runserver","0.0.0.0:80"]