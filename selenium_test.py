from selenium.webdriver.support.ui import Select
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

def parse_links():
    driver = webdriver.Firefox()
    driver.get("https://jaomix.ru/category/tri-zhizni-smert-ne-u-reki-zabveniya/") #link on manga/ranobe on jaomix.ru for example "https://jaomix.ru/lenivyj-mechnik/""
    try:
        data = ''
        select = Select(driver.find_element_by_xpath("(//select[@class='sel-toc new-ajax-load'])"))
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

        soup = BeautifulSoup(visibletab.get_attribute('innerHTML'))
        for a in soup.find_all('a', href=True):
            data+=str('https://jaomix.ru'+a['href']+'\n')

        links = open("links.txt","w",encoding='utf8') #File with links
        links.write(data)
        links.close()

def download_from_links():
    textfile = open("links.txt") #Import file with links
    lines = textfile.readlines()
    tex = ''

    for line in reversed(lines):
        text = open("text.txt","a",encoding='utf8') #File with ready text
        url = line.rstrip()
        headers= {"User-Agent":"Mozilla/5.0"} #Headers for safety
        r = requests.get(url, headers=headers)

        data = r.text
        data1 = data.encode('UTF-8')
        soup = BeautifulSoup(data1)

        st1=soup.find("h1", {'class': 'entry-title'}) #Номер главы
        st2=soup.find("div", {'class': 'entry-content'}) #Содержание
        full_text=(st1.text + ' ' + (st2.text).replace('Услуга "Убрать рекламу".Теперь мешающую чтению рекламу можно отключить!', ''))

        correcting = full_text.replace('Если вы обнаружите какие-либо ошибки ( неработающие ссылки, нестандартный контент и т.д.. ), Пожалуйста, сообщите нам об этом , чтобы мы могли исправить это как можно скорее.', '')

        text.write(correcting+'\n')
        text.close()

parse_links()
download_from_links()