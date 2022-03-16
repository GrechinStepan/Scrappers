from selenium import webdriver
from openpyxl import Workbook
from bs4 import BeautifulSoup
from time import sleep
import os


#СБОР СТРАНИЦЫ
def get_data(url):
        PATH = '' 
        driver = webdriver.Chrome(PATH)

        driver.get(url=url)
        
        sleep(10)
        
        pageSource = driver.page_source
        
        fileToWrite = open("page_source.html", "w", encoding="utf-8")
        fileToWrite.write(pageSource)
        fileToWrite.close()
        
        driver.quit()
        get_info()


def get_info():             
        wb = Workbook()
        ws = wb.active
        ws.append(['Дом', 'Номер кв.', 'Этаж', 'Кол-во комн.', 'Площадь', 'Планировка', 'Цена'])
        
        fileToRead = open("page_source.html", "r", encoding="utf-8")
        soup = BeautifulSoup(fileToRead, 'lxml')
        cards = soup.find_all('div', class_='v-search-card')

        for card in cards:
                plan = 'https://veer-park.ru' + card.find('img', class_='v-search-card_image_room').get('src')

                num = card.find('div', class_='v-search-card_header').get_text().split(' ')[1].replace('№', '')

                price = card.find('div', class_='v-search-card_button_text').get_text().replace(' ', '').replace('₽', '')
              
                room_count = card.find('div', class_='v-search-card_header').get_text()                
                if '1-комн.' in room_count: 
                        room = '1'
                elif '2-комн.' in room_count:
                        room = '2'
                elif '3-комн.' in room_count:
                        room = '3'
                else:
                        room = '0'
                
                params = card.find_all('div', class_='v-search-card_about_item')
                for param in params:
                        if 'Площадь' in param.get_text():
                                size = param.get_text().split(' ')[1].replace('.', ',')
                        if 'Этаж' in param.get_text():
                                floor = param.get_text().split(' ')[1].replace('/25', '')
                        if 'Дом' in param.get_text():
                                house = param.get_text().split(' ')[1].replace('№', '')
        
                ws.append([house, num, floor, room, size, plan, price])
        wb.save(f'') 
       
def main():
        get_data('https://veer-park.ru/filter/') # Ссылка на сайт 
        os.remove('')
main()        

