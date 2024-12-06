# News Parser

Скрипт для парсинга новостей с использованием NewsAPI, с сохранением данных в PostgreSQL и экспортом в Excel.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/news-parser.git
   cd news-parser
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` и добавьте настройки:

   ```env
   NEWS_API_KEY=your_news_api_key
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=your_db_name
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   ```

## Использование

Запустите скрипт с параметрами: ключевое слово и максимальное количество статей:

```bash
python scripts/parse_data.py <keyword> <max_articles>
```

**Пример**:

```bash
python pars_data.py "technology" 10
```

### Параметры:

- `keyword` — ключевое слово для поиска новостей.
- `max_articles` — максимальное количество статей для сохранения.

## Результат

- Новости сохраняются в базе данных PostgreSQL и в Excel-файл (`news_<keyword>.xlsx`).
- Логи выполнения записываются в `news_parser.log`.

## Примечания

- Для работы с PostgreSQL установите [PostgreSQL](https://www.postgresql.org/).
- Получите [API-ключ для NewsAPI](https://newsapi.org/).