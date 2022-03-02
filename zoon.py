import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import random
from openpyxl import Workbook

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    
def get_data(url):  
    PATH = 'C:\\Users\\grech\\Desktop\\работа\\chromedriver\\chromedriver'
    driver = webdriver.Chrome(PATH)
    
    try:
        driver.get(url=url)
        time.sleep(3)
        
        while True:
            find_more_element = driver.find_element(By.CLASS_NAME, "catalog-button-showMore")
            
            if driver.find_elements(By.CLASS_NAME, "hasmore-text"):
                with open("C:\\Users\\grech\\Desktop\\работа/source-page.html", "a", encoding="utf-8") as file:
                    file.write(driver.page_source)
                    
                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()
                time.sleep(5)          
    except Exception as _ex:
        print(_ex)   
    finally:
        driver.close()
        driver.quit()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    

def info():   
    wb = Workbook()
    ws = wb.active 
    start = time.time()
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 Safari/537.36',
            }
    proxies = {
            'http': 'http://109.172.110.232:49155',
            }
    with open('source-page.html', 'r', encoding="utf-8") as f:
        src = f.read()        
        soup = BeautifulSoup(src, "lxml")
        cards = soup.find_all('li', class_='minicard-item')
        name_no = ['kfc', 'макдоналдс', 'бургер кинг', 'ресторан быстрого питания pizza mia', 'subway', 'burger king', 'шашлыкофф', 'шоколадница', 'додо пицца', 'вилка-ложка', 'il патио', 'тануки', 'поль бейкери', 'суши точка', 'суши wok', 'папа джонс', 'своя компания', 'starbucks']
        names = []
        rest_urls = [] 
        
        for card in cards:
            rating_value = float(card.find("span", class_="rating-value").get_text().replace(',', '.'))
            comments = float(card.find('div', class_='comments').get_text(strip = True).split(' ')[0])
            name = card.find('h2').get_text(strip=True).lower()        
            if 0 < rating_value <= 3.8 and comments >= 20 and name not in name_no and names.count(name) == 0: 
                names.append(name)               
                rest_urls.append(card.find('a', class_='title-link').get('href'))
        
        for r in rest_urls:
            list = []
            req_rest = requests.get(r, headers = headers).text
            rest_soup = BeautifulSoup(req_rest, 'lxml')

            try:
                phone_list = []
                item_phones = rest_soup.find("div", class_="service-phones-list").find_all("a", class_="js-phone-number")
                for phone in item_phones:
                    item_phone = str(phone.get("href").replace('tel:', ''))
                    phone_list.append(item_phone)
            except:
                item_phone = 'NO'

            if len(phone_list) == 0:
                continue
            else:
                item_name = rest_soup.find("span", {"itemprop": "name"}).text.strip()
                
                item_rating = rest_soup.find('span', class_='rating-value').text.strip()

                item_comments = rest_soup.find('a', class_='fs-large gray js-toggle-content').text.strip().split(' ')[0]
                
                for google in range(0, 21, 10):
                    google_req = requests.get(f'https://www.google.ru/search?q={item_name}+екатеринбург+отзывы&newwindow=1&sxsrf=APq-WBtQhfES1q0ER23OSQsfceDJlFa84A:1644637010982&ei=UisHYu-rO4SnrgSvva3wCQ&start={google}&sa=N&ved=2ahUKEwjvnMumnvn1AhWEk4sKHa9eC54Q8NMDegQIARBN&biw=1565&bih=1274&dpr=0.75' , headers = headers, proxies=proxies).text
                    time.sleep(random.randrange(15,50))
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
                            rat_google = float(rat_google.split('·')[0].strip().replace('Рейтинг: ', '').replace(',', '.'))
                            if rat_google <= 3.9:
                                if 'zoon' in plat:
                                    platform = 'зун'
                                elif 'tripadvisor' in plat:
                                    platform = 'трип'
                                elif 'restaurantguru' in plat:
                                    platform = 'гуру'
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
                ws.append(['Екатеринбург', item_name, item_name, r, '; '.join(phone_list), f'{item_rating}/{item_comments}', ' '.join(list)])
                print(item_name, list ) 

    wb.save('/Users/grech/Desktop/работа/Екатеринбург.xlsx')
    end = time.time()
    print(f'Обработано за {(end - start) // 60} минут')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    

def main():
    hood = ['akademicheskij', 'avtovokzal', 'botanika', 'verh-isetskij', 'viz', 'evropejskij', 'vtuzgorodok', 'vtorchermet', 'vokzalnyj', 'vizovskij', 'koltsovo', 'kirovskij', 'zarechnyj', 'zheleznodorozhnyj', 'zhbi',]
    for h in hood:
        get_data(f'https://ekb.zoon.ru/restaurants/?search_query_form=1&require_comments=1&districts%5B%5D={h}')
    
    info()



# https://ekb.zoon.ru/restaurants/?search_query_form=1&require_comments=1&districts%5B%5D=akademicheskij
# https://ekb.zoon.ru/restaurants/?search_query_form=1&require_comments=1&districts%5B%5D=avtovokzal