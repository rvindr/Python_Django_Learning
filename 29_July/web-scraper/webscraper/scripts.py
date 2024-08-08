from bs4 import BeautifulSoup
import requests

def scraper_imdb_news():
    url =' https://www.imdb.com/news/movie/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'

    }

    response = requests.get(url, headers = headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    new_items = soup.find_all('div', class_ = 'ipc-list-card--border-line ipc-list-card sc-bec740f7-0 bLjVWt ipc-list-card--base')

    for item in new_items:
        title = item.find('a', class_ = 'ipc-link ipc-link--base sc-bec740f7-3 gBbzGe')
        desc = item.find('div', class_='ipc-html-content-inner-div')
        img = item.find('img', class_="ipc-image")
        external_link = title['href']

        title = title.text.strip() if title else "No Title"
        desc = desc.text.strip() if desc else "No desc"
        img = img['src'] if img else None

        articles.append({
            'title' : title,
            'desc' : desc,
            'img' : img,
            'external_link' : external_link
        })
        return articles

scraper_imdb_news()