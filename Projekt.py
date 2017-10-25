import requests
import re
import os
import csv

stadiums_url = 'https://en.wikipedia.org/wiki/List_of_stadiums_by_capacity'
stadiums_directory = 'stadiums'
frontpage_filename = 'stadiums.html'

def download_url_to_string(url):
    try:
        r = requests.get(url)
    except:
        print('failed to download url' + url)
        return None
    return r.text

def get_url(url):
    try:
        r = requests.get(url)
    except:
        print('failed to download url' + url)
        return None
    return r

def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    
    with open(path, 'w') as f:
        f.write(text)
    return None

def save_url_to_a_file():
    text = download_url_to_string(stadiums_url)
    
    #t = text.encode(encoding="utf-8")
    save_string_to_file(text, stadiums_directory, frontpage_filename)
    return None

