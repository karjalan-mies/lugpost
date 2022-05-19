from datetime import datetime
from os import makedirs, path
from pathlib import Path
from random import randint

from bs4 import BeautifulSoup
import requests
from transliterate import translit

from main import get_html


def translit_it(text: str) -> str:
    return translit(text, language_code="ru", reversed=True)


def process_text(text: str) -> str:
    text = translit_it(text)
    text = text.lower().replace(':', '').replace('\'', '')
    text = text.strip().replace(' ', '_')
    return text


def remove_line_break(text: str) -> str:
    return text.replace('\r\n', ' ')


def get_unique_file_name(file_path: str) -> str:
    if path.exists(file_path):
        only_path = path.split(file_path)[0]
        file_name, file_ext = path.splitext(path.split(file_path)[-1])
        new_file_name = file_name + str(randint(10000, 99999)) + file_ext
        new_path = Path() / only_path / new_file_name
        return get_unique_file_name(new_path)
    else:
        return file_path


def save_image(img_file, file_name: str) -> str:
    if not path.exists('Photo'):
        makedirs('Photo')
    file_path = Path() / 'Photo' / file_name
    file_path = get_unique_file_name(file_path)
    with open(file_path, 'wb') as f:
        f.write(img_file.content)
    return file_name


def get_image(soup: str) -> tuple:
    try:
        img_url = soup.find('img', class_='xfieldimage foto', src=True)['src']
        file_name = img_url.split("/")[-1]
        img_file = requests.get(f'http://lugpost.ru{img_url}')
        return img_file, file_name
    except(TypeError):
        print('The image does not exist')
        return '', ''


def get_persons_photo(soup: str) -> None:
    img_file, file_name = get_image(soup)
    if img_file:
        file_name = save_image(img_file, file_name)
    return file_name


def get_profile_data(soup: str) -> str:
    people_profile = soup.find('div', class_='full-text video-box clearfix')
    people_profile = people_profile.findAll('b')
    profile = {}
    for item in people_profile:
        if item.text and item.find_next('font').text:
            cleared_item = remove_line_break(item.find_next('font').text)
            profile[process_text(item.text)] = cleared_item
    return profile


def get_people_data(url: str) -> dict:
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    image_file_name = get_persons_photo(soup)
    number_of_name_values = len(soup.find('h1').text.split())
    if number_of_name_values == 3:
        l_name, f_name, patronymic = soup.find('h1').text.split()
    elif number_of_name_values == 2:
        l_name, f_name = soup.find('h1').text.split()
        patronymic = ''
    else:
        print('The name has more than 3 values\n' +
              f'{soup.find("h1").text}')
        return False
    people_info = {}
    people_info['data_sozdaniya'] = datetime.now().strftime('%d.%m.%Y')
    people_info['istochnik_informacii'] = 'lugpost.ru'
    people_info['familiya'] = l_name
    people_info['imya'] = f_name
    people_info['otchestvo'] = patronymic
    profile = get_profile_data(soup)
    if 'data_rozhdenija' in profile:
        people_info['data_rozhdenija'] = profile['data_rozhdenija']
    people_info['imya_faila'] = image_file_name
    people_info['papka'] = 'Photo'
    return people_info


if __name__ == '__main__':
    get_people_data()
