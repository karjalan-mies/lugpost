import os
from pathlib import Path

from bs4 import BeautifulSoup
import requests
from transliterate import translit


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0)' +
                      'Gecko/20100101 Firefox/45.0'
          }


def translit_it(text: str)-> str:
    return translit(text, language_code="ru", reversed=True)


def process_text(text: str) -> str:
    text = translit_it(text)
    text = text.lower().replace(':', '').replace('\'', '')
    text = text.strip().replace(' ', '_')
    return text


def get_html(url):
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Network error!')
        return False


def get_and_save_image(soup):
    try:
        img_url = soup.find('img', class_='xfieldimage foto', src=True)['src']
        # print(img_url)
        img_file = requests.get(f'http://lugpost.ru{img_url}')

        if not os.path.exists('Photo'):
            os.makedirs('Photo')

        file_name = img_url.split("/")[-1]
        file_path = Path() / 'Photo' / file_name
        with open(file_path, 'wb') as f:
            f.write(img_file.content)
        return file_name
    except(TypeError):
        print('The image does not exist')


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
    file_name = get_and_save_image(soup)
    l_name, f_name, patronymic = soup.find('h1').text.split()
    people_info = {}
    people_info['last_name'] = l_name
    people_info['first_name'] = f_name
    people_info['patronymic'] = patronymic
    profile = get_profile_data(soup)
    people_info = {**people_info, **profile}
    people_info['file_name'] = file_name
    return people_info


if __name__ == '__main__':
    get_people_data()
