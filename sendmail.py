import smtplib, ssl
#siehe https://realpython.com/python-send-email/

def main():
    send_mail("Dies ist ein Test")


def send_mail(message):
    port = 465
    password = "passwort"
    sender_email = "xyz@gmail.com"
    receiver_email = "xyz@gmail.com"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

if __name__ == "__main__":
    main()
