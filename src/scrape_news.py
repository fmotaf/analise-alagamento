import requests
from bs4 import BeautifulSoup
import sqlite3
import time

ALAGAMENTO_SEARCH_URL = 'https://www.acordacidade.com.br/page/{}/?s=alagamento'
DATABASE = 'articles.db'
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "cookie": "hgyclh-w8a60=25204dee62cb3733039a27bbcfb758a8; seox-lgpd-cookies=true; ym_periodical_actions={}",
    "if-modified-since": "Sun, 25 May 2025 18:10:16 GMT",
    "priority": "u=0, i",
    "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

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
        if response.status_code != 200:
            print(f"Erro HTTP {response.status_code} ao acessar {url}")
            return ""
        soup = BeautifulSoup(response.content, 'html.parser')

        content_div = soup.find('article', class_='g-col-12 lg:g-col-8 xl:g-col-8')
        if not content_div:
            print(f"Conteúdo não encontrado em {url}")
            # Debug: Salva o HTML para análise
            with open('debug.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            return ""
        return content_div.get_text(separator=" ", strip=True)
    except Exception as e:
        print(f"Erro ao obter conteúdo de {url}: {e}")
        return ""

def store_article_in_db(url, content, db_name):
    print(url)
    print(f"conteudo recebido = {content[:30]}...")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS noticias (url TEXT PRIMARY KEY, content TEXT)')
    cursor.execute('UPDATE noticias SET content = ? WHERE url = ? AND content IS NULL', (content, url))
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
