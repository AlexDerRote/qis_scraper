from htmlparser import qis
from time import sleep
from datetime import datetime
from sendmail import send_mail
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
#Dateneingabe:
#---------------------------------------------------
username = "xy1234z"
password = "1234topsecret%?"
#---------------------------------------------------

def main():
    eingetragene_klausuren_saved = 0
    table_open = []
    table_result = []
    old_table = []
    i = 0
    while 1:
        errorcode = "NONE"
        time = datetime.now()
        print(f"Zeitstempel: {time}")
        if time.hour >= 8 and time.hour <= 22: #Zeiten in denen qis-Scraper läuft
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                scraper = qis()
                offene_klausuren, rows_open, eingetragene_klausuren, rows_result = scraper.check_klausuren(username=username, password=password)
                table_open = qis.sort_table(rows_open)
                table_result = qis.sort_table(rows_result)
                
                print("------------------------------------------------")
                print(f"Es stehen Ergebnisse für {offene_klausuren} Klausuren aus.")
                print("------------------------------------------------")
                for row in table_open:
                    print(f"ModulNr: {row[0]} | Fach: {row[1]}")

                notenliste = []
                print("------------------------------------------------")
                print(f"Ergebnisse für {eingetragene_klausuren} Klausuren sind bereits eingetragen.")
                print("------------------------------------------------")
                for row in table_result:
                    zeile = f"{row[6]} mit {row[4]} | Fach: {row[1]} | ECTS: {row[5]}"
                    notenliste+=zeile
                    notenliste+="\n"
                notenliste = ''.join(notenliste[0:len(notenliste)-1])
                print(notenliste)
                print("------------------------------------------------")

                check_num_of_results(eingetragene_klausuren, eingetragene_klausuren_saved, table_result, table_open, notenliste)
                eingetragene_klausuren_saved = eingetragene_klausuren
                old_table = table_result
                i += 1
                print(f"Anzahl der Checks: {i}")
                
            except TimeoutException:
                print("Timeout Exception...")
                print("ist der QIS - Server erreichbar?")
                errorcode = "00x504"
            except NoSuchElementException:
                print("NoSuchElementException Exception...")
                print("ist der QIS - Server erreichbar?")
                errorcode = "00x503"

                
            finally:
                print("In fünf Minuten erneut überprüfen...")
                print("------------------------------------------------")
        else:
            print("Das Programm wird erst um 8 Uhr wieder gestartet...")
            
        sleep(300)
    

def check_num_of_results(eingetragene_klausuren, eingetragene_klausuren_saved, table_result, table_open, notenliste): # Sendet Email an Benutzer (siehe sendmail.py)
    if eingetragene_klausuren != eingetragene_klausuren_saved:
        if eingetragene_klausuren_saved == 0:
            message = ("Subject: QIS Scraper gestartet\n\n"
                "Eingetragene Pruefungsleistungen: {}\n"
                "Ausstehende Pruefungsleistungen: {}\n\n"
                       "{}").format(len(table_result), len(table_open), notenliste)
            send_mail(message)
        else:
            message = ("Subject: NEUE KLAUSURERGEBNISSE VEROEFFENTLICHT!\n\n"
                       "Im QIS wurden neue Klausurergebnisse hinterlegt.\n\n"
                       "{}").format(notenliste)
            send_mail(message)
            print("neue Klausurergebnisse online")
    else:
        print("keine neuen Prüfungsergebnisse")


def compareTables(table1, table2):
    for row1 in table1:
        i=0
        for row2 in table2:
            if row1[0] == row2[0]:
                i = 1
                break
            else:
                pass
        if i == 0:
            klausurergebnis = row1
            return klausurergebnis
        else:
            pass
    


if __name__ == "__main__":
    main()
    pass
