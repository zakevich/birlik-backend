# apilog-backend

Here is the step-by-step guidance how to run backend locally from scratch

## install modules

`pip install -r requirements.txt`

## run docker

`docker compose -f "deploy/local/docker-compose.yml" up -d`

## create super user

`python manage.py createsuperuser`

## run migrations

python manage.py makemigrations

`python manage.py migrate`

## run backend

`python manage.py runserver 0.0.0.0:8080`

## open web-site

http://localhost:8080/admin/

for local
Username: birliq
Email address: test@birliq.kz
Password: birliq
