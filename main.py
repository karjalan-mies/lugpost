import csv
import os
import requests

from bs4 import BeautifulSoup

from config import FIELDS, HEADERS, URL
from parsers import get_people_data


def get_html(url: str) -> str:
    try:
        result = requests.get(url, headers=HEADERS)
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
        people_data = get_people_data(link)
        if people_data:
            lugpost_data.append(people_data)
    save_to_file(lugpost_data)


def create_file():
    with open('export_data.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fields=FIELDS, delimiter=';')
        writer.writeheader()


def save_to_file(lugpost_data: list) -> None:
    if not os.path.exists('export_data.csv'):
        create_file()
    with open('export_data.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fields=FIELDS, delimiter=';')
        for person in lugpost_data:
            writer.writerow(person)


if __name__ == '__main__':
    html = get_html(URL)
    if html:
        get_lugpost_data(html)
    for i in range(2, 74):
        html = get_html(f'{URL}/page{i}/')
        get_lugpost_data(html)
    print('The program was successfully completed.')
