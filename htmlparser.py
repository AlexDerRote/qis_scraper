from selenium import webdriver
import os  
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options

#path = '/home/qis/qis-alarm/chromedriver'

class qis:
    #INIT
    def __init__(self):
        self.url = "https://www.qis.fh-aachen.de/qisserver/rds?state=user&type=0&topitem=&breadCrumbSource=portal&topitem=functions"
        #self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0), john@doe.com', 'Referer' : 'https://www.google.com/'}
    #END OF INIT

    def start_browser():
        options = webdriver.FirefoxOptions()
        options.headless = True
        options.firefox_binary="/usr/bin/firefox-esr"

        return webdriver.Firefox(options=options)
        
    def check_klausuren(self, username, password):
        
        """Öffnet die QIS Website und sucht die offenen Klausuren heraus

        Args:
            username (string): Die FH-ID für das QIS z.B.: ab1234s
            password (string): Passwort für die FH Dienste

        Returns:
            int, <list>: Anzahl der offenen Klausuren, Datenreihen mit Klausurinformationen
        """
        print("Starte QIS - Reader ...")

        dr = qis.start_browser()
        dr.get(url=self.url)

        userBox = dr.find_element_by_id("asdf")
        userBox.send_keys(username)

        passwordBox = dr.find_element_by_id("fdsa")
        passwordBox.send_keys(password)

        button = dr.find_element_by_id("loginForm:login")
        button.click()

        #dr.implicitly_wait(2)
        print("Erfolgreich eingeloggt..")

        exam_button = dr.find_element_by_link_text('Info über angemeldete Prüfungen')
        exam_button.click()

        #dr.implicitly_wait(2)

        dr.find_element_by_xpath('//*[@title="angemeldete Prüfungen anzeigen für Bachelor - Fahrzeug- und Antriebstechnik  (PO-Version 2018) "]').click()
        #Muss auf jeweiligen Studiengang angepasst werde. Hierzu im QIS das HTML Objekt untersuchen
        
        print("Daten werden gesammelt ..")

        #dr.implicitly_wait(2)
        time.sleep(1)


        soup = bs(dr.page_source, 'lxml')

        table = soup.find_all('table')[1] 
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        austehende_klausuren = len(rows) - 2 #Minus 2 wegen table headers

        dr.close()

        return austehende_klausuren, rows

    def sort_table(rows):
        data = []
        rows.pop(0)
        rows.pop(0)
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data



