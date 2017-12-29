import requests
import re
import os

# import csv


stadiums_url = 'https://en.wikipedia.org/wiki/List_of_stadiums_by_capacity'
stadiums_directory = 'stadiums'
frontpage_filename = 'stadiums.html'


def download_url_to_string(url):
    '''his function takes a URL as argument and tries to download it
        using requests. Upon success, it returns the page contents as string.
    '''
    try:
        # there is no error
        r = requests.get(url)
    except:
        # some error
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
    '''Write "text" to the file "filename" located in directory "directory",
        creating "directory" if necessary. If "directory" is the empty string, use
        the current directory.
    '''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return None


def save_url_to_a_file():
    '''Save "stadiums_url" to the file "stadiums_directory"/"frontpage_filename"'''
    text = download_url_to_string(stadiums_url)
    save_string_to_file(text, stadiums_directory, frontpage_filename)
    return None


def read_file_to_string(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.'''
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


def stadiums(page):
    '''function returns list of tuples.'''
    rx = re.compile(r'<tr>'
                    r'.+?'
                    # name of stadium
                    r'<td><a .+?>(?P<name_of_stadium>.*?)</a>.?.?.?.?.?.?.?</td>'
                    r'.+?'
                    # stadium capacety
                    r'<td>(?P<capacitet_of_stadium>\d{2,3},\d\d\d).+?</td>'
                    r'.+?'
                    # city where is stadium
                    r'<td><a .*?>(?P<city_where_is_stadium>.+?)</a></td>'
                    r'.+?'
                    # country where is stadium
                    r'<td>(?P<country_where_is_stadium>.+?)</td>'
                    r'.+?'
                    # which team trains at stadium
                    r'<td><a .*?>(?P<team_that_trains_at_stadium>.+?)</a>.*?</td>'
                    r'.+?'
                    # main use of stadium
                    r'<td>.*?</td>'
                    r'.+?'
                    r'</tr>'
                    ,
                    re.DOTALL)
    note = re.findall(rx, page)
    return note


print(stadiums(read_file_to_string(stadiums_directory, frontpage_filename)))
