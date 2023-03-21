from bs4 import BeautifulSoup
import requests


urls = []
with open("list of id's.txt", 'r') as f:
    urls.extend(_.strip() for _ in f.readlines())

BASE_URL = 'https://help.steampowered.com/pl/wizard/HelpWithGameTechnicalIssue?appid='


def scrape_data(url):
    data = {
        'Game_ID': '',
        'Steam_game_url': '',
        'Customer_service_page': '',
        'Product_page': '',
        'Email': '',
        'Publisher': '',
        'Publisher_url': '',
        'Producer': '',
        'Producer_url': ''
    }
    response = requests.get(BASE_URL + url)
    soup = BeautifulSoup(response.text, 'lxml')

    sub = soup.find('div', class_='help_official_box')
    data['Game_ID'] = url
    data['Steam_game_url'] = BASE_URL + url
    try:
        customer = sub.find('div', class_='help_whitelight_text help_official_support_row').find('a')['href']
        data['Customer_service_page'] = customer
    except:
        data['Customer_service_page'] = ''
    try:
        product_page = sub.find('div', class_='help_official_support_row help_whitelight_text').find('a')['href']
        data['Product_page'] = product_page
    except:
        data['Product_page'] = ''
    try:
        email = soup.find('div', class_='help_official_support_row').find_next('span',
                                                                           class_='help_whitelight_text').next_element.next_element
        data['email'] = email.strip(' : ')
    except:
        data['email'] = ''
    try:
        second_email = soup.find('div', class_='help_official_support_row').find_next('span',
                                                                           class_='help_whitelight_text').next_element.next_element.next_element
        data['second_email'] = second_email.strip(' : ')
    except:
        data['second_email'] = ''
    try:
        publisher = sub.find_next('div', class_='subbox').find_next('div', class_='subbox')
        data['Publisher'] = ' '.join(publisher.text.split()[1:])
        data['Publisher_url '] = publisher.find('a')['href']
    except:
        data['Publisher'] = ''
        data['Publisher_url '] = ''
    try:
        producer = sub.find_next('div', class_='subbox').find_next('div', class_='subbox').find_next('div',
                                                                                                     class_='subbox')
        data['Producer'] = ' '.join(producer.text.split()[1:])
        data['Producer_url'] = producer.find('a')['href']
    except:
        data['Producer'] = ''
        data['Producer_url'] = ''

    return data
