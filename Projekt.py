import requests
import re
import os
#import csv

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

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return None


def save_url_to_a_file():
    text = download_url_to_string(stadiums_url)
    save_string_to_file(text, stadiums_directory, frontpage_filename)
    return None


def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


def page_to_table(page):
    rx = re.compile(r'<tr>'
                    r'(.*?)'
                    r'<td><a href="(\w+)" title="(\w+)">(?P<title_of_stadium>.+?)</a></td>'
                    r'(.*?)'
                    r'<td>(?P<capacity_of_stadium>.+?)<sup (.*?)></td>'
                    r'(.*?)'
                    r'<td><a(.*?)>(?P<city_where_is_stadium>.+?)</a></td>'
                    r'(.*?)'
                    r'<td>(?P<country_where_is_stadium>.+?)</td>'
                    r'(.*?)'
                    r'<td><a href="(.*?)" title="(.*?)">(?P<team_that_trains_at_stadium>.+?)</a>(.*?)</td>'
                    r'(.*?)'
                    r'</tr>',
                    re.DOTALL)
    stadiums = re.search(rx, page)
    return stadiums

table = page_to_table(read_file_to_string(stadiums_directory, frontpage_filename))

