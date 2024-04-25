import smtplib
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def send_email(send_to: str, header: str, body: str):  

    msg = MIMEMultipart()
    msg['From'] = config.SEND_FROM_EMAIL
    msg['To'] = send_to
    msg['Subject'] = header

    msg.attach(MIMEText(body, 'plain'))
    sender = smtplib.SMTP("smtp.gmail.com", 587)
    sender.starttls()
    sender.login(config.SEND_FROM_EMAIL, config.PASSWORD_EMAIL)
    text = msg.as_string()
    sender.sendmail(msg['From'], msg['To'], text)

    sender.quit()
