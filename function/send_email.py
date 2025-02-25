from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib


def send_email(sender_email, sender_password, recipient_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message))

        server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
        server.ehlo(sender_email)
        server.login(sender_email, sender_password)
        server.auth_plain()
        server.send_message(msg)
        server.quit()

        print("Сообщение успешно отправлено!")
    except Exception as e:
        print(f"Возникла ошибка при отправке сообщения: {e}")


# Пример использования функции send_email
send_email(
    "cukanovartem8258@yandex.ru",
    "Artem_0907",
    "cukanovartem2008@gmail.com",
    "google.com",
    "Your code is 6208",
)
