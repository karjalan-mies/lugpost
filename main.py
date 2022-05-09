import requests
from bs4 import BeautifulSoup
from pprint import pprint

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Network error!')
        return False


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    peoples = soup.find('div',
                        id='dle-content').findAll('div',
                                                  class_='news-item2 clearfix')
    for people in peoples:
        full_name = people.find('a', class_='news-item-title2').text
        print(full_name)
    # pprint(peoples)


if __name__ == '__main__':
    html = get_html('https://lugpost.ru/vprestupleniya/')
    if html:
        get_data(html)
