import os
import requests
import argparse
from dotenv import load_dotenv
from datetime import datetime
from openpyxl import Workbook
from bs4 import BeautifulSoup
import psycopg2
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("news_parser.log")
    ]
)

load_dotenv()

api_key = os.getenv('NEWS_API_KEY')
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')


def connect_to_db(db_name=db_name):
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        return conn
    except Exception as e:
        logging.error(f"Ошибка при подключении к базе данных: {e}")
        return None


def clean_html_text(text):
    return ' '.join(BeautifulSoup(text, "html.parser").get_text(separator=" ").split())


def process_article_data(article):
    article['description'] = clean_html_text(article['description'])
    if not article['description'] or len(article['description']) < 500:
        logging.debug(
            f"Описание слишком короткое. Загружаем полный текст для: {article['url']}")
        article['description'] = get_full_article(
            article['url']) or article['description']
    return article


def get_full_article(url):
    try:
        logging.info(f"Пытаемся перейти по ссылке: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            logging.info(
                f"Запрос к {url} успешен! Статус: {response.status_code}")
            encoding = response.encoding if response.encoding != 'ISO-8859-1' else 'utf-8'
            text = response.content.decode(
                encoding, errors='replace').encode('utf-8').decode('utf-8')
            soup = BeautifulSoup(text, 'html.parser')
            article_text = ''
            article_element = soup.find('div', class_='article-body')
            if article_element:
                article_text = article_element.get_text(strip=True)
            else:
                paragraphs = soup.find_all('p')
                for p in paragraphs:
                    article_text += p.get_text(strip=True) + '\n'
            return article_text.strip()
        else:
            logging.info(
                f"Ошибка при запросе: {url}. Статус код: {response.status_code}")
            return ""
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при загрузке страницы: {e}")
        return ""


def get_news(api_key, query='tech', language='ru', sort_by='publishedAt', page_size=10, max_articles=10):
    url = f'https://newsapi.org/v2/everything?q={query}&language={language}&sortBy={sort_by}&pageSize={page_size}&apiKey={api_key}'
    try:
        logging.info(f"Выполняем запрос к API: {url}")
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json()['articles']
        logging.info(f"Получено {len(articles)} статей от API.")

        articles = [process_article_data(article) for article in articles]

        # Ограничиваем количество релевантных статей
        if len(articles) > max_articles:
            articles = articles[:max_articles]

        logging.info(
            f"Ограничено количество статей до {max_articles}. Всего статей: {len(articles)}.")
        return articles
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        return []


def save_news_to_excel(articles, filename='data/news.xlsx'):
    try:
        logging.info(f"Сохраняем новости в файл Excel: {filename}")
        wb = Workbook()
        ws = wb.active
        ws.append(["Заголовок", "Описание", "Ссылка",
                  "Источник", "Дата публикации"])
        for article in articles:
            published_at = datetime.strptime(
                article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ") if article['publishedAt'] else None
            ws.append([article['title'], article['description'],
                      article['url'], article['source']['name'], published_at])
        wb.save(filename)
        logging.info(f"Файл {filename} успешно сохранен.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении файла Excel: {e}")


def create_news_table():
    conn = connect_to_db()
    if not conn:
        logging.error("Не удалось подключиться к базе данных.")
        return
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS public.news
        (
            title text NOT NULL,
            description text NOT NULL,
            url text NOT NULL PRIMARY KEY,
            source_name text NOT NULL,
            published_at TIMESTAMP NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Таблица 'news' успешно создана в базе данных.")


def save_news_to_db(articles):
    conn = connect_to_db()
    if not conn:
        logging.error("Не удалось подключиться к базе данных.")
        return
    cursor = conn.cursor()
    for article in articles:
        try:
            article = process_article_data(article)
            published_at = datetime.strptime(
                article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ") if article['publishedAt'] else None
            cursor.execute("""
                INSERT INTO news (title, description, url, source_name, published_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) 
                DO UPDATE SET 
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    source_name = EXCLUDED.source_name,
                    published_at = EXCLUDED.published_at;
            """, (article['title'], article['description'], article['url'], article['source']['name'], published_at))
            conn.commit()
            logging.info(
                f"Статья '{article['title']}' успешно сохранена в базу данных.")
        except Exception as e:
            logging.error(
                f"Ошибка при сохранении статьи '{article['title']}': {e}")
    cursor.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Парсер новостей.")
    parser.add_argument('keyword', type=str,
                        help="Ключевое слово для поиска новостей.")
    parser.add_argument('max_articles', type=int,
                        help="Максимальное количество статей для сохранения.")

    args = parser.parse_args()

    search_keyword = args.keyword
    max_articles = args.max_articles

    logging.info(
        f"Ищем новости по ключевому слову: {search_keyword} с ограничением в {max_articles} статей.")
    articles = get_news(api_key, query=search_keyword,
                        language='ru', max_articles=max_articles)

    if articles:
        logging.info(f"Получено {len(articles)} новостей.")
        save_news_to_excel(articles, filename=f"data/news_{search_keyword}.xlsx")
        save_news_to_db(articles)
    else:
        logging.warning("Новости не были получены.")


if __name__ == "__main__":
    create_news_table()
    main()
