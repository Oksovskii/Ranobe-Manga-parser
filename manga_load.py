from selenium.webdriver.support.ui import Select
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from progress.bar import IncrementalBar

def parse_links():
    print("Инициализация вебдрайвера...")
    driver = webdriver.Firefox()
    print("Вебдрайвер инициализирован")
    driver.get(input('Введите ссылку для скачивания с "jaomix.ru": ')) #link on manga/ranobe on jaomix.ru for example "https://jaomix.ru/lenivyj-mechnik/""
    print("Получение ссылок глав...")
    try:
        data = ''
        select = Select(driver.find_element_by_xpath("(//select[@class='sel-toc new-ajax-load'])"))
        print(select.options)
        for element in select.options:
            element.click()
            time.sleep(0.1) #Delay for safety

            visibletab = driver.find_element_by_xpath('//div[@class="hiddenstab active"]')

            soup = BeautifulSoup(visibletab.get_attribute('innerHTML'))
            for a in soup.find_all('a', href=True):
                data+=str('https://jaomix.ru'+a['href']+'\n')

        links = open("links.txt","w",encoding='utf8') #File with links
        links.write(data)
        links.close()
    except:
        visibletab = driver.find_element_by_xpath('//div[@class="hiddenstab active"]')

        soup = BeautifulSoup(visibletab.get_attribute('innerHTML'),"html.parser")
        for a in soup.find_all('a', href=True):
            data+=str('https://jaomix.ru'+a['href']+'\n')

        links = open("links.txt","w",encoding='utf8') #File with links
        links.write(data)
        links.close()
        print("Ссылки получены")

def download_from_links():
    textfile = open("links.txt") #Import file with links
    lines = textfile.readlines()
    tex = ''

    with open('links.txt') as f:
        size=len([0 for _ in f])
    print("Запись глав")
    bar = IncrementalBar('Глав записано:', max = size)

    for line in reversed(lines):
        text = open("text.txt","a",encoding='utf8') #File with ready text
        url = line.rstrip()
        headers= {"User-Agent":"Mozilla/5.0"} #Headers for safety
        r = requests.get(url, headers=headers)

        data = r.text
        data1 = data.encode('UTF-8')
        soup = BeautifulSoup(data1,"html.parser")

        st1=soup.find("h1", {'class': 'entry-title'}) #Номер главы
        st2=soup.find("div", {'class': 'entry-content'}) #Содержание
        full_text=(st1.text + ' ' + (st2.text).replace('Услуга "Убрать рекламу".Теперь мешающую чтению рекламу можно отключить!', ''))

        correcting = full_text.replace('Если вы обнаружите какие-либо ошибки ( неработающие ссылки, нестандартный контент и т.д.. ), Пожалуйста, сообщите нам об этом , чтобы мы могли исправить это как можно скорее.', '')

        text.write(correcting+'\n')
        text.close()
        bar.next()
    bar.finish()
    print("Главы записаны и доступны в файле 'text.txt'")

parse_links()
download_from_links()
