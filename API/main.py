import QrCodeGenerationService as Qr
import MailSendService as Sender


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Qr.generatecode("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "", "name")
    Sender.sendmail("jeandaniel.spadazzi@epsi.fr", "./name.png")

