from django.shortcuts import render, redirect
from scraper.models import News
import os
import uuid
from urllib3 import request
# Create your views here.
def index(request):
    context = {'news':News.objects.all()}
    return render(request, 'index.html', context)


from bs4 import BeautifulSoup
import requests

def scraper_imdb_news(request):
    url =' https://www.imdb.com/news/movie/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'

    }

    response = request.get(url, headers = headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.find_all('div', class_ = 'ipc-list-card--border-line ipc-list-card sc-bec740f7-0 bLjVWt ipc-list-card--base')

    for item in news_items:
        title = item.find('a', class_ = 'ipc-link ipc-link--base sc-bec740f7-3 gBbzGe')
        desc = item.find('div', class_='ipc-html-content-inner-div')
        img = item.find('img', class_="ipc-image")
        external_link = title['href']

        title = title.text.strip() if title else "No Title"
        desc = desc.text.strip() if desc else "No desc"
        img = img['src'] if img else 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVLDP5s2j9u1x86fOb7kNKXanJeMn8zZ30ZQ&s'
        img_path = None

        if img:
            img_name = f'image_{uuid.uuid4()}.jpg'
            img_path = download_img(img, 'downloads', img_name)
        
        news = {
            'title' : title,
            'desc' : desc,
            'img' : img,
            'external_link' : external_link
        }

        News.objects.create(**news)




def download_img(img_url, save_directory, img_name):

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    img_path = os.path.join(save_directory, img_name)
    response = requests.get(img_url, stream=True)

    if response.status_code == 200:
        with open(img_name,'wb') as file:
            for chunck in response.iter_content(1024):
                file.write(chunck)

    return img_url