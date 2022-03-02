import requests
from bs4 import BeautifulSoup
from time import sleep
import time
from openpyxl import Workbook


def get_data(url):
    start = time.time()
    wb = Workbook()
    ws = wb.active
    name_no = ['KFC', 'Макдональдс', 'Бургер Кинг', 'Pizza Mia', 'Subway', 'Burger King']
    name = []
    for t in range(270,10901,30):
        print(t)
        
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 YaBrowser/22.1.0.2517 Yowser/2.5 Safari/537.36'
            }
        
        req = requests.get(url + f'o=a{t}', headers = headers).text
        sleep(5)
        
        soup = BeautifulSoup(req, 'lxml')
        cards = soup.find_all('div', class_='cauvp Gi o')

        rest_url = []

        for c in cards:           
            try:
                rating_v_karte = c.find('div', class_='bhDlF bPJHV').find('a', class_='dMdkg _S').find('svg', class_='RWYkj d H0').get('title')
                kolvo_otz = int(c.find('span', class_='NoCoR').get_text().replace(' отзывов', '').replace(' отзыва', '').replace(' отзыв', ''))
                name_ok = c.find('a', class_='bHGqj Cj b').get_text().split('.')[-1].strip() 
                if '3,5' in rating_v_karte or '3,0' in rating_v_karte or '2,5' in rating_v_karte or '2,0' in rating_v_karte or '1,5' in rating_v_karte or '1,0' in rating_v_karte:  
                    if kolvo_otz >= 20:
                        if name.count(name_ok) <= 3 and name_ok not in name_no:
                            rest_url.append('https://www.tripadvisor.ru' + c.find('div', class_='bhDlF bPJHV').find('a', class_='dMdkg _S').get('href'))
                            name.append(name_ok)
                            
            except:
                continue
        print('добавлено компаний ' + f'{len(name) - 6}')
        for r in rest_url:
            req_card = requests.get(r, headers = headers).text
            card_soup = BeautifulSoup(req_card, 'lxml')
            card = card_soup.find('div', class_='page')

#название
            nazvanie = card.find('h1', class_='fHibz').get_text()
#количество отзывов
            kolvo_otzivov = card.find('a', class_='dUfZJ').get_text().replace('отзыва', '').replace('отзыв', '')
#рейтинг
            rating = card.find('svg', class_='RWYkj d H0').get('title').replace(' из 5 кружков', '')
#телефон
            try:
                telefon = card.find('div', class_='bKBJS Me').find('span', class_='brMTW').get_text()
            except:
                telefon = 'нет'
#почта          
            try:
                mail = card.find_all('div', class_='bKBJS Me enBrh')
                for m in mail:
                    pochta = str(m.find('a').get('href')).replace('mailto:', '').replace('?subject=?', '')
            except:
                pochta = '-'
            
            if telefon == 'нет':
                continue
            else:
                ws.append(['Питер', nazvanie, nazvanie, f'{rating}/{kolvo_otzivov}', r, telefon, pochta])           

    wb.save('/Users/grech/Desktop/работа/moscow.xlsx')
    end = time.time()
    print(end - start)
get_data('https://www.tripadvisor.ru/RestaurantSearch?Action=PAGE&ajax=1&availSearchEnabled=false&sortOrder=popularity&geo=298484&itags=10591&')