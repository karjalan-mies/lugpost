from os import makedirs, path
from pathlib import Path
from random import randint

from bs4 import BeautifulSoup
import requests
from transliterate import translit


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0)' +
                      'Gecko/20100101 Firefox/45.0'
          }


def translit_it(text: str) -> str:
    return translit(text, language_code="ru", reversed=True)


def process_text(text: str) -> str:
    text = translit_it(text)
    text = text.lower().replace(':', '').replace('\'', '')
    text = text.strip().replace(' ', '_')
    return text


def get_unique_file_name(file_path):
    if path.exists(file_path):
        only_path = path.split(file_path)[0]
        file_name, file_ext = path.splitext(path.split(file_path)[-1])
        new_file_name = file_name + str(randint(1, 9)) + file_ext
        print(new_file_name)
        new_path = Path() / only_path / new_file_name
        return get_unique_file_name(new_path)
    else:
        return file_path


def save_image(img_file, file_name):
    if not path.exists('Photo'):
        makedirs('Photo')

    file_path = Path() / 'Photo' / file_name
    file_path = get_unique_file_name(file_path)
    with open(file_path, 'wb') as f:
        f.write(img_file.content)
    return file_name


def get_image(soup):
    try:
        img_url = soup.find('img', class_='xfieldimage foto', src=True)['src']
        file_name = img_url.split("/")[-1]
        img_file = requests.get(f'http://lugpost.ru{img_url}')
        return img_file, file_name
    except(TypeError):
        print('The image does not exist')
        return ['', '']


def get_persons_photo(soup: str) -> None:
    img_file, file_name = get_image(soup)
    if img_file:
        file_name = save_image(img_file, file_name)
    return file_name


def get_profile_data(soup):
    people_profile = soup.find('div', class_='full-text video-box clearfix')
    people_profile = people_profile.findAll('b')
    profile = {}
    for element in people_profile:
        if element.text and element.find_next('font').text:
            profile[process_text(element.text)] = element.find_next('font').text
    return profile


def get_people_data(link):
    people_data = requests.get(link, headers=headers)
    soup = BeautifulSoup(people_data.text, 'html.parser')
    file_name = get_persons_photo(soup)
    l_name, f_name, patronymic = soup.find('h1').text.split()
    people_info = {}
    people_info['familiya'] = l_name
    people_info['imya'] = f_name
    people_info['otchestvo'] = patronymic
    profile = get_profile_data(soup)
    people_info = {**people_info, **profile}
    people_info['file_name'] = file_name
    return people_info


if __name__ == '__main__':
    get_people_data()
