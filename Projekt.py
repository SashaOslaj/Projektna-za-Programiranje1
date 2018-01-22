import requests
import re
import os
import csv
import json

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
                    r'</tr>'
                    ,
                    re.DOTALL)
    note = re.findall(rx, page)
    return note


def stadium(sez):
    new_list = []
    num = 0
    for i in sez:
        if num != 0:
            new_list.append(i)
        else:
            num += 1
    return new_list


def razclenjeni_stadioni(sez):
    '''Function from file frontpage returns list of stadiums.'''
    new_list = []
    rx = re.compile(r'<td><a href="/wiki/.*?" title="(?P<name>.*?)">.*?</a>.*?</td>'
                    r'.+?'
                    r'<td>(?P<capacity>\d{2,3},\d\d\d).*?</td>'
                    r'.+?'
                    r'<td>(<a href=".*?" title=".+?">)?(?P<city_where_is_stadium>.*?)(</a>.*?)?</td>'
                    r'.+?'
                    r'<td>(<.*?>)?(?P<country_where_is_stadium>.*?)(</.*?>)?</td>'
                    r'.+?'
                    r'<td>(<.*?>)?(?P<team_that_trains_at_stadium>.*?)(<.*?>.*?)?</td>'
                    r'.+?'
                    r'<td>(<a .*?>)?(?P<main_use1>.*?)(</a>)?'
                    r'(,? (and)? (<a .*?>)?(?P<main_use2>.*?)(</a>)?)?'
                    r'(, (<a .*?>)?(?P<main_use3>.*?)(</a>)?)?'
                    r'(, (<a .*?>)?(?P<main_use4>.*?)(</a>)?.?)?'
                    r'(((, (<a .*?>)?(?P<main_use5>.+?)(</a>)?)?))</td>'
                    , re.DOTALL
                    )
    for i in sez:
        nabor = re.findall(rx, i)
        dolzina = 0
        for y in nabor:
            dolzina += len(y)
        # print(dolzina)
        for y in nabor:
            #            print(y)
            new_list.append((y[0], y[1], y[3], y[6], y[9], y[12], y[21], y[25], y[31], y[32]))
    return new_list


# ['name', 'capacity', 'city', 'country', 'team', 'use']

def slovar_stadionov(sez):
    l = []
    for nabor in sez:
        stadion = {}
        for i, j in enumerate(nabor):
            if i == 0:
                stadion['name'] = j
            if i == 1:
                stadion['capacity'] = j
            if i == 2:
                stadion['city'] = j
            if i == 3:
                stadion['cauntry'] = j
            if i == 4:
                stadion['team'] = j
            if i == 5:
                stadion['use'] = [j]
            if i > 5:
                if j != '':
                    stadion['use'].append(j)
        l.append(stadion)
    return l


def zapisi_json(podatki, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        json.dump(podatki, datoteka, indent=2)

# podatki = ['name', 'capacity', 'city', 'country', 'team', 'use']
stadioni = stadium(stadiums(read_file_to_string(stadiums_directory, frontpage_filename)))
# print(stadioni)
# seznam = razclenjeni_stadioni(stadioni)
# print(len(seznam))
# print(seznam)
# print(slovar_stadionov(seznam))
# json_dat = zapisi_json(slovar_stadionov(seznam), 'stadiums.json')
# csv_dat = write_stad_csv(slovar_stadionov(seznam))
