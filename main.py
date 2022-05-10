from wsgiref import headers
import requests
from bs4 import BeautifulSoup

from test import get_people_data


def get_html(url):
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Network error!')
        return False


def get_people_link(people) -> str:
    link = people.find('a', class_='news-item-title2')['href']
    return link


def get_data(data):
    all_data = []
    with open(data, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    people = soup.find('div',
                       id='dle-content').findAll('div',
                                                 class_='news-item2 clearfix')
    for person in people:
        link = get_people_link(person)
        all_data.append(get_people_data(link))
    print(all_data)


if __name__ == '__main__':
    # html = get_html('https://lugpost.ru/vprestupleniya/')
    # if html:
    get_data('data.html')
