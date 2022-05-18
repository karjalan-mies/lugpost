import csv
import requests

from bs4 import BeautifulSoup

from parsers import get_people_data


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0)' +
                      'Gecko/20100101 Firefox/45.0'
          }


def get_html(url: str) -> str:
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Network error!')
        return False


def get_person_link(person: str) -> str:
    link = person.find('a', class_='news-item-title2')['href']
    return link


def get_lugpost_data(html: str) -> list:
    lugpost_data = []
    soup = BeautifulSoup(html, 'html.parser')
    people = soup.find('div',
                       id='dle-content').findAll('div',
                                                 class_='news-item2 clearfix')
    for person in people:
        link = get_person_link(person)
        lugpost_data.append(get_people_data(link))
    save_to_file(lugpost_data)


def save_to_file(lugpost_data: list):
    with open('export_data.csv', 'w', encoding='utf-8', newline='') as f:
        fields = ['familiya', 'imya', 'otchestvo', 'data_rozhdenija',
                  'mesto_rozhdenija', 'dejatelnost', 'punkt_obvinenija',
                  'facebook', 'twitter', 'vk', 'dopolnitelnaja_informatsija',
                  'file_name', ]
        writer = csv.DictWriter(f, fields, delimiter=';')
        writer.writeheader()
        for person in lugpost_data:
            writer.writerow(person)


if __name__ == '__main__':
    html = get_html('https://lugpost.ru/vprestupleniya/')
    if html:
        get_lugpost_data(html)
    print('The program was successfully completed.')
