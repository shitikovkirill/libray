# Library

## Run dev

```bash
docker compose up
```

## Run test
```bash
docker compose -f docker-compose.yaml -f docker-compose.test.yaml up app --build
```

## Run prod

```bash
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up --build
```
