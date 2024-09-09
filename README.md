# sale_agent


### Запускаем докер
`docker-compose --env-file .env up --build `

## Alembic
### Устанавливаем алембик
`pip install alembic`

### Редактируем файл alembic.ini 
`sqlalchemy.url = driver://user:pass@localhost/dbname`

значения из .env, например:

`sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/reviews`

### Применяем миграции
`alembic upgrade head` 

### Посмотрим историю миграций 
`alembic history `


## Объктная модель (сущности)

![schema.png](./readme_files/schema.png)

