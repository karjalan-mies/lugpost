from bs4 import BeautifulSoup
import requests

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }


def get_html(url):
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Network error!')
        return False


def get_people_data():
    with open('people_data.html', 'r') as f:
        people_data = f.read()

    soup = BeautifulSoup(people_data, 'html.parser')
    
    img_url = soup.find('img', class_='xfieldimage foto', src=True)['src']
    img_file = requests.get(f'http://lugpost.ru{img_url}')
    file_name = img_url.split('/')[-1]
    with open(file_name, 'wb') as f:
        f.write(img_file.content)
    l_name, f_name, patronymic = soup.find('h1').text.split()
    
    people_info = soup.find('div',
                            class_='full-text video-box clearfix')
    people_profile = people_info.findAll('b')
    for element in people_profile:
        if element.text and element.find_next('font').text:
            element_value = element.find_next('font').text
            print(f'{element.text} {element_value}')
    print(f'Имя файла: {file_name}')
    print(f'Фамилия: {l_name}\nИмя: {f_name}\nОтчество: {patronymic}')


if __name__ == '__main__':
#     html = get_html(
# 'https://lugpost.ru/vprestupleniya/124394-budaevskiy-anton-olegovich.html')
#     if html:
#         with open('people_data.html', 'w', encoding='utf-8') as f:
#             f.write(html)
    get_people_data()
