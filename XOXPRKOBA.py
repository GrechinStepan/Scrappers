from selenium import webdriver
from openpyxl import Workbook
from bs4 import BeautifulSoup
from time import sleep
import os


def get_data():
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        PATH = 'C:\\Users\\grech\\Desktop\\работа\\chromedriver\\chromedriver' #небходимо сменить директорию на ту, в которой будет лежать ХРОМДРАЙВЕР
        driver = webdriver.Chrome(PATH, options=options)
        
        #Драйвер по очереди открывает две сслыки (1я шахматка, 2я планировки) и записывает в два временных файла
        url_list = ['https://domnahohryakova.ru/#/macrocatalog/houses/1576451/bigGrid?studio=null&floorNum=8&category=flat&activity=sell&presMode=house', 'https://domnahohryakova.ru/#/macrocatalog/houses/1576451/plans?studio=null&floorNum=2&category=flat&activity=sell&presMode=house']
        for url in range(len(url_list)):
                fileToWrite = open(f"page{url}.html", "w", encoding="utf-8")
                driver.get(url = url_list[url])
                sleep(10)
                pageSource = driver.page_source    
                fileToWrite.write(pageSource) 
                fileToWrite.close()
                
        driver.quit() 

def get_info():             
        wb = Workbook()
        ws = wb.active
        ws.append(['Дом', 'Подъезд', 'Этаж', 'Кол-во комн.', 'Площадь', 'Планировка', 'Цена'])
        
# Чтение первого временного файла для сбора основной инфы
        fileToRead = open("page0.html", "r", encoding="utf-8")
        soup = BeautifulSoup(fileToRead, 'lxml')
        cards = soup.find_all('div', class_='item-box bg-search')

# Чтение второго временного файла для сбора планировок
        fileToRead = open("page1.html", "r", encoding="utf-8")
        soup2 = BeautifulSoup(fileToRead, 'lxml')
        cards2 = soup2.find_all('div', class_='plan_item')

# Сбор планировок
        plan_list = []
        price_list = []
        for card2 in cards2:
                plan_list.append(card2.find('div', class_='plan_image').get('style').replace('background-image: url("', '').replace('?");', ''))
                price_list.append(card2.find('div', class_='plan_price pull-left').get_text(strip=True).replace(' ', '').replace('₽', '').split('.')[0])

# Сбор инфы
        for card in cards:
                price = card.find('div', class_='item-box-price').get_text().replace(' ', '').replace('₽', '')
                
                rooms = card.find('div', class_='item-box-rooms').get_text().replace('К', '')
                
                area = card.find('span', class_='item-box-area').get_text().replace(' м²', '')
                
                # площадь и колво комнат заключено в ссылку планировок, поэтому он находит совпадения и выводит подходящую планировку
                for pl in plan_list:
                        if area.replace(',', '.') in pl and f'k{rooms}' in pl:
                                p = pl
                
                house = card.find('div', class_='item-box-number').get_text(strip = True).split('-')[0].replace('№', '').split('.')[0]

                entrance = card.find('div', class_='item-box-number').get_text(strip = True).split('-')[0].replace('№', '').split('.')[1]

                floor = card.find('div', class_='item-box-number').get_text(strip = True).split('-')[1]
        
                



                ws.append([house, entrance, floor, rooms, area, p, price])
        
        wb.save(f'/Users/grech/Desktop/ХОХРЯКОВА.xlsx')
        

def main():
        get_data()
        get_info()
        os.remove('C:\\Users\\grech\\Desktop\\работа\\page0.html') # Необходимо сменить путь, по которму будет удаляться файл page0.html
        os.remove('C:\\Users\\grech\\Desktop\\работа\\page1.html') # Необходимо сменить путь, по которму будет удаляться файл page1.html

main()

