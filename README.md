# Instalation

### basic necessities
---
for local developement
- install python 3
- create new dir in where you want your new project to live
- install [virtualenv tool](https://pypi.org/project/virtualenv/) on your system
- virtual environment will isolate the project environment and dependecies for your project from the rest of your system
- run:
    - the first command will create folder for virtual environment called venv with python binaries and pip - package install manager
```sh
$ virtualenv venv -p python3
$ cd venv
$ source bin/activate
```
- ```source bin activate``` will activate the virtualenv or ```source Scripts/activate``` for Windows

### how to create django project and install dependencies
---
While in your project folder (home/--->project folder/)
run:
```sh
$ pip install -r requirements.txt
```
- that will install all dependencies that are in the `requirements.txt` file

Continue with seting up the main django project and the application you want it to have
```sh
$ django-admin startproject {name of project}
```
- enter project folder and run
```sh
$ django-admin startapp {name of the app}
```
- First commands start new Django project and second one new app (avoid calling your application an `app` - It confuses Django on some occasions depending on IDEs. You might have to rewrite some files.)

You should create .env file in root folder or your project which acts as storage for env variables that is easy to maintain and should be gitignored. It can hold `secrets` like password to your DB and django project SECRET KEY and other secrets. In production your should use Key/Management system. I have used python-dotenv library in settings.py only for ilustration how it works.


# Running local server and migrations
---
When you create new model in your app or make changes to it, or download project with some models you have to synchronise it with your database
- open up terminal in your IDE/OS and go to folder where manage.py resides\
run:
```sh
$ ./manage.py migrate
```
to synchronize DB with current model state or
```sh
$ ./manage.py makemigrations
```
if you made changes to your model, than migrate

You can run ```./manage.py check``` that everything in your project is OK

Prior to running Django server, you need to run ```./get_offers_token.sh``` script, which will fetch access_token to communicate with 'Offers' microservice and save it to you local .env file.

For running the local server and checking your Django is ok run:
```sh
$ ./manage.py runserver {you can add port number after, by default its 8000}
```

Than visit http://127.0.0.1:8000 in your browser
