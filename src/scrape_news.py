import requests
from bs4 import BeautifulSoup
import sqlite3
import time

ALAGAMENTO_SEARCH_URL = 'https://www.acordacidade.com.br/page/{}/?s=alagamento'
DATABASE = 'articles.db'

def get_news_links(pages=3):
    links = set()
    for page in range(1, pages + 1):
        url = ALAGAMENTO_SEARCH_URL.format(page)
        print(f'Raspando página de busca: {url}')
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('https://www.acordacidade.com.br/') and 'alagamento' in href:
                links.add(href)
        time.sleep(1)
    return list(links)

def fetch_article_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', class_='post-content') or soup.find('div', class_='content')
        if not content_div:
            return ""
        return content_div.get_text(separator=" ", strip=True)
    except Exception as e:
        print(f"Erro ao obter conteúdo de {url}: {e}")
        return ""

def store_article_in_db(url, content, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS noticias (url TEXT PRIMARY KEY, content TEXT)')
    cursor.execute('INSERT OR IGNORE INTO noticias (url, content) VALUES (?, ?)', (url, content))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    news_links = get_news_links(pages=5)
    print(f"{len(news_links)} links encontrados.")

    for link in news_links:
        print(f"Coletando: {link}")
        content = fetch_article_content(link)
        store_article_in_db(link, content, db_name=DATABASE)
