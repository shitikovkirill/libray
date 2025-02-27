# Library

[Svagger url](http://localhost:8000/docs/)

## Run dev

```bash
docker compose up  --build
```

## Run test
```bash
docker compose -f docker-compose.yaml -f docker-compose.test.yaml up --build
```

## Run manage.py

```bash
docker compose exec app python manage.py
```

## Run prod

```bash
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up --build
```


# Procfile
web: gunicorn myproject.wsgi --log-file -

# requirements.txt
django
gunicorn
whitenoise
django-heroku
psycopg2-binary

# runtime.txt
python-3.9.12

# command for deploy
heroku login
heroku create my-django-app
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a my-django-app
heroku buildpacks:set heroku/python
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set DJANGO_SETTINGS_MODULE=myproject.settings.prod
heroku config:set SECRET_KEY='your-secret-key'
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku open