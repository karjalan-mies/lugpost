from wsgiref import headers
import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Network error!')
        return False


def get_full_name(people):
    link = people.find('a', class_='news-item-title2')['href']
    return link


def get_data(html):
    with open(html, 'r') as f:
        data = f.read()

    soup = BeautifulSoup(data, 'html.parser')
    peoples = soup.find('div',
                        id='dle-content').findAll('div',
                                                  class_='news-item2 clearfix')
    for people in peoples:
        link = get_full_name(people)
        print(link)
    # pprint(peoples)


if __name__ == '__main__':
    # html = get_html('https://lugpost.ru/vprestupleniya/')
    # if html:
    get_data('data.html')
