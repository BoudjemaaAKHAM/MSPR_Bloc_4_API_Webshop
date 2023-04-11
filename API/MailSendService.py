import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def sendmail(target, img):

    with open(img, 'rb') as i:
        img_data = i.read()

    sender = "guillaume.gay.74@gmail.com"
    msg = MIMEMultipart()
    msg['Subject'] = 'subject'
    msg['From'] = sender
    msg['To'] = sender
    text = MIMEText("Ceci est un email de Test")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(img))
    msg.attach(image)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "cybkqequeqtxfyic")
    server.set_debuglevel(1)
    server.sendmail(sender, target, msg.as_string())
    server.quit()
