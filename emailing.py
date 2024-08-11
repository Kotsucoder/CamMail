import os
import smtplib
import imghdr
import glob
from email.message import EmailMessage

PASSWORD = os.getenv("PASSWORD")
SENDER = "ENTER YOUR OWN EMAIL"
RECIEVER = "ENTER YOUR OWN EMAIL"
still_sending = False
cleaning = False

def clean_folder():
    global cleaning
    if not cleaning:
        print("clean_folder function started")
        cleaning = True
        images = sorted(glob.glob("images/*.png"))[1:]
        for image in images:
            os.remove(image)
        print("clean_folder function ended")
        cleaning = False
        return True
    else:
        print("Hold on!")
        return False

def send_email(image_path):
    global still_sending
    if not still_sending:
        print("send_email function started")
        still_sending = True
        email_message = EmailMessage()
        email_message["Subject"] = "New customer showed up!"
        email_message.set_content("Hey, we just saw a new customer!")

        with open(image_path, "rb") as file:
            content = file.read()
        email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

        gmail = smtplib.SMTP("smtp.gmail.com", 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(SENDER, PASSWORD)
        gmail.sendmail(SENDER, RECIEVER, email_message.as_string())
        gmail.quit()
        print("send_email function ended")
        still_sending = False
        clean_folder()
    else:
        print("Global Variable Worked!")


if __name__ == "__main__":
    send_email(image_path="images/0.png")