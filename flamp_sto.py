import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from time import sleep
import time
import random



def get_data(url, page, city_rus):
    start = time.time()
    wb = Workbook()
    ws = wb.active  
    names = [] 
    count = 0
    for p in range(1, page):
        print(f'Обрабатывается страница № {p}')
        headers = {
                'user-agent': '',
                }
        

        proxies = {
                'http': '',
                }
                    
        req = requests.get(url + f'{p}', headers = headers, proxies=proxies).text
        sleep(5)
        soup = BeautifulSoup(req, 'lxml')
        cards = soup.find_all('li', class_='list-cards__item list-cards__item--card')

        sto_url = []
        
        for c in cards:
            rating = float(c.find('cat-brand-filial-rating').get('rating'))
            reviews_count = int(c.find('cat-brand-filial-rating').get('reviews-count'))
            name = c.find('a', class_='card__link').get_text().strip().lower()

            if 0 < rating <= 3.8 and reviews_count >= 20 and names.count(name) <= 1:
                names.append(name)
                sto_url.append('https:' + c.find('a', class_='card__link').get('href'))
        
        for r in sto_url:
            list = [] 
            req_sto = requests.get(r, headers = headers).text
            sto_soup = BeautifulSoup(req_sto, 'lxml')
            sto = sto_soup.find('div', class_='l-content l-content--basic l-content--bg-white t-text')

            try:
                mobila = []
                nt = sto.find_all('a', class_='link filial-phones__number')
                for n in nt:
                    mobila.append(n.get_text().replace('\n\t\t\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t\t\t', ''))
                if len(mobila) == 0:
                    mobila = 'нет'
            except:
                mobila = 'нет'
                continue
            
            if mobila == 'нет':
                continue
            else:
                nazvanie = sto.find('h1', class_='header-filial__name t-h3').get_text().strip()

                kolvo_otzivov = sto.find('a', class_='filial-rating__reviews link js-hash-link').get_text(strip = True).split(' ')[0]

                rat = sto.find('cat-brand-filial-rating').get('rating')
                
                try:
                    sfera = sto.find('div', 'header-filial__subtitle t-text').get_text().strip()
                except:
                    sfera = ' '
                
                try:
                    kolvo_filialov = int(sto.find('a', class_='filial-location__all link is-not-expandable js-all-filials-link').get_text(strip=True).split(' ')[1])
                    kolvo_filialov = str(kolvo_filialov + 1)
                except:
                    kolvo_filialov = '1'

    #Сбор с гугла           
                for google in range(0, 21, 10):
                    google_req = requests.get(f'https://www.google.ru/search?q={sfera}+{nazvanie}+{city_rus}+отзывы&newwindow=1&sxsrf=APq-WBtQhfES1q0ER23OSQsfceDJlFa84A:1644637010982&ei=UisHYu-rO4SnrgSvva3wCQ&start={google}&sa=N&ved=2ahUKEwjvnMumnvn1AhWEk4sKHa9eC54Q8NMDegQIARBN&biw=1565&bih=1274&dpr=0.75' , headers = headers, proxies=proxies).text
                    sleep(random.randrange(15,50))
                    soup = BeautifulSoup(google_req, 'lxml')
                    
                    try:
                        google_rating = float(soup.find('div', class_='Ob2kfd').find('span', class_='Aq14fc').get_text().replace(',', '.'))
                        if google_rating <= 3.9:
                            list.append('гугл')
                            list.append(str(google_rating))
                    except:
                        google_rating = 'не найдено'
                    
                    cards_google = soup.find_all('div', class_='jtfYYd')                   
                    for cg in cards_google:
                        try:               
                            plat = cg.find('cite', class_='iUh30 qLRx3b tjvcx').get_text()
                            rat_google = cg.find('div', class_='fG8Fp uo4vr').get_text()
                            rat_google = float(rat_google.split('·')[0].strip().replace('Рейтинг: ', '').replace(',', '.').replace('%', ''))
 
                            if rat_google <= 3.9:
                                if 'zoon' in plat:
                                    platform = 'зун'
                                elif '2gis' in plat:
                                    platform = 'гис'
                                elif 'yandex' in plat:
                                    platform = 'ян'
                                elif 'yell' in plat:
                                    platform = 'йел'
                                elif 'otzovik' in plat:
                                    platform = 'отз'
                                elif 'irecommend' in plat:
                                    platform = 'рек'
                                elif 'sprav' in plat:
                                    platform = 'справ'
                                elif 'asktel' in plat:
                                    platform = 'аск'                        
                                else:
                                    continue 
                                if platform not in list:
                                    list.append(platform)
                                    list.append(str(rat_google))
                                                        
                        except:
                            continue

            if len(list) == 0:
                continue
            else:
                ws.append([city_rus, sfera, nazvanie, nazvanie, r, '; '.join(mobila), kolvo_filialov, f'{rat}/{kolvo_otzivov}', ' '.join(list)])
                count += 1
                print(count, nazvanie, kolvo_filialov, list ) 
    
    wb.save(f'/Users/grech/Desktop/работа/{city_rus} ({count}).xlsx')
    end = time.time()
    print(f'Обработано за {(end - start) // 60} минут')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')            



def main():
    city_list = ['nnovgorod', 'chelyabinsk']
    pages = [100, 150]
    city_list_rus = ['Новгород', 'Челябинск']
    if len(city_list) == len(pages) == len(city_list_rus):
        for cities in range(len(city_list)):
            url = f'https://{city_list[cities]}.flamp.ru/metarubric/sto?page='
            page = pages[cities]
            city_rus = city_list_rus[cities]
            get_data(url, page, city_rus)
    else:
        print('ОШИБКА')

main()

