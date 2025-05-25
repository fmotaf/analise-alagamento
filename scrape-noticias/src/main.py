import requests
from bs4 import BeautifulSoup
import sqlite3

ALAGAMENTO_URL = 'https://www.acordacidade.com.br/?s=alagamento'
DATABASE = 'noticias.db'
def get_news_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('https://www.acordacidade.com.br/') and 'alagamento' in href:
            links.append(href)
    return links

def store_links_in_db(link, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS links (url TEXT)')

    cursor.execute('INSERT INTO links (url) VALUES (?)', link)

    conn.commit()
    conn.close()

def analyze_links(links):
    # i need to analyze the links and check if they contain useful data



if __name__ == '__main__':
    news_links = get_news_links(ALAGAMENTO_URL)
    for link in news_links:
        store_links_in_db(link, db_name=DATABASE)