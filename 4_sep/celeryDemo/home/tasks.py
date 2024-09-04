from celery import shared_task
import time
import os
import requests

@shared_task
def add(x, y):
    time.sleep(13)
    return x + y


@shared_task
def download_img(img_url, save_directory, img_name):

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    img_path = os.path.join(save_directory, img_name)
    response = requests.get(img_url, stream=True)

    if response.status_code == 200:
        with open(img_path,'wb') as file:
            for chunck in response.iter_content(1024):
                file.write(chunck)

    return img_url