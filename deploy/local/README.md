1. Install the requirements to virtual env:

```aiignore
pip install -r requirements.txt
```

2. Create .env file locally:

```.env
   DATABASE_PASSWORD=local
```

3. Start the django app (port 8080)

```aiignore
python manage.py runserver 0.0.0.0:8080
```

4. Start the docker with DB (port 5432) and Nginx (port 8888):

```aiignore
cd deploy/local
docker-compose up -d
```

5. Start the front-end from its directory (port 5173)

```aiignore
 npm run dev -- --host 0.0.0.0
```

6. Create admin user:

```aiignore
 python manage.py createsuperuser
```

7. Verify that backend and frontend are running behind nginx:

BE http://localhost:8888/admin
FE http://localhost:8888/#/

