# Library

## Run dev

```bash
docker compose up
```

## Run test
```bash
docker compose -f docker-compose.yaml -f docker-compose.test.yaml up app --build
```

## Run manage.py

```bash
docker compose exec app python manage.py
```

## Run prod

```bash
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up --build
```
