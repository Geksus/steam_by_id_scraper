import concurrent.futures
import csv

import requests
from bs4 import BeautifulSoup

urls = []
with open("list of id's.txt", 'r') as f:
    urls.extend(_.strip() for _ in f.readlines())

urls.sort()
l = len(urls)

BASE_URL = 'https://help.steampowered.com/pl/wizard/HelpWithGameTechnicalIssue?appid='

data = {
        'Game_ID': '',
        'Game_name': '',
        'Steam_game_url': '',
        'Customer_service_page': '',
        'Product_page': '',
        'Email': '',
        'Second_email': '',
        'Publisher': '',
        'Publisher_url': '',
        'Producer': '',
        'Producer_url': ''
    }
fieldnames = data.keys()


def scrape_data(url):
    data = {
        'Game_ID': '',
        'Game_name': '',
        'Steam_game_url': '',
        'Customer_service_page': '',
        'Product_page': '',
        'Email': '',
        'Second_email': '',
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
        data['Game_name'] = soup.find('div', class_='subbox_left').text.strip()
    except:
        data['Game_name'] = ''
    try:
        product_page = sub.find('div', class_='help_official_support_row help_whitelight_text').find('a')['href']
        data['Product_page'] = product_page
    except:
        data['Product_page'] = ''
    try:
        email = soup.find('div', class_='help_official_support_row').find_next('span',
                                                                           class_='help_whitelight_text').next_element.next_element
        data['Email'] = email.strip(' : ')
    except:
        data['Email'] = ''
    try:
        second_email = soup.find('div', class_='help_official_support_row').find_next('span',
                                                                           class_='help_whitelight_text').next_element.next_element.next_element
        data['Second_email'] = second_email.strip(' : ')
    except:
        data['Second_email'] = ''
    try:
        publisher = sub.find_next('div', class_='subbox').find_next('div', class_='subbox')
        data['Publisher'] = ' '.join(publisher.text.split()[1:])
        data['Publisher_url'] = publisher.find('a')['href']
    except:
        data['Publisher'] = ''
        data['Publisher_url'] = ''
    try:
        producer = sub.find_next('div', class_='subbox').find_next('div', class_='subbox').find_next('div',
                                                                                                     class_='subbox')
        data['Producer'] = ' '.join(producer.text.split()[1:])
        data['Producer_url'] = producer.find('a')['href']
    except:
        data['Producer'] = ''
        data['Producer_url'] = ''

    print(f"Processed {urls.index(url)} of {l}")

    return data


def scrape_urls(urls):
    with concurrent.futures.ThreadPoolExecutor(30) as executor:
        results = executor.map(scrape_data, urls)
    return list(results)


def write_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for d in data:
            writer.writerow(d)


def main():
    results = scrape_urls(urls)
    write_to_csv('new_results.csv', results)

if __name__ == '__main__':
    main()
