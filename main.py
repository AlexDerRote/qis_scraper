from htmlparser import qis
from time import sleep
from datetime import datetime
from sendmail import send_mail
from selenium.common.exceptions import TimeoutException, NoSuchElementException
#Dateneingabe:
#---------------------------------------------------
username = "ab1234s"
password = "Passwort123%"
#---------------------------------------------------

def main():
    offene_klausuren_saved = 0
    table = []
    old_table = []
    i = 0
    while 1:
        errorcode = "NONE"
        time = datetime.now()
        print(f"Zeitstempel: {time}")
        if time.hour >= 8 and time.hour <= 20: #QIS-Scraper wird nur waehrend der Oeffnungszeiten des PA gestartet
            try:
                scraper = qis()
                offene_klausuren, rows = scraper.check_klausuren(username=username, password=password)
                table = qis.sort_table(rows)
                
                print("------------------------------------------------")
                print(f"Es stehen Ergebnisse für {offene_klausuren} Klausuren aus.")
                print("------------------------------------------------")

                for row in table:
                    print(f"ModulNr: {row[0]} | Fach: {row[1]}")

                check_open_exams(offene_klausuren, offene_klausuren_saved, old_table, table)
                offene_klausuren_saved = offene_klausuren
                old_table = table
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
                print("In einer Stunde erneut überprüfen...")
                print("------------------------------------------------")
        else:
            print("Das Programm wird erst um 8 Uhr wieder gestartet...")
            
        sleep(2700)
    



def check_open_exams(offene_klausuren, offene_klausuren_saved, old_table, new_table): # Sendet Email an Benutzer (siehe sendmail.py)
    if offene_klausuren != offene_klausuren_saved:
        if offene_klausuren_saved == 0:
            message = """\
Subject: QIS Scraper gestartet

Diese Nachricht wurde automatisch generiert."""
            #send_mail(message)
        else:
            message = """\
            Subject: NEUE KLAUSURERGEBNISSE VEROEFFENTLICHT!

            Im QIS wurden neue Klausurergebnisse hinterlegt."""
            #send_mail(message)
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
