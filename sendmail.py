import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scraping import scraping
import os
from dotenv import load_dotenv

load_dotenv()
gmail_address = os.getenv('GMAIL')
gmail_password = os.getenv('GMAILPASSWORD')
recipient = [gmail_address]


def sendmail():
    dataframe = scraping()
    msg = MIMEMultipart()
    msg['Subject'] = "Banking Jobs In MyJobMag"
    msg['From'] = gmail_address
    html = """\
            <html>
              <head></head>
              <body>
                {0}
              </body>
            </html>
    """.format(dataframe.to_html(index=False))
    part1 = MIMEText(html, 'html')
    msg.attach(part1)
    try:
        # Checking for connection errors
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_address, gmail_password)
        server.sendmail(msg['From'], recipient, msg.as_string())
        server.close()
        print('Email sent successfully')
    except Exception as e:
        print("Error for connection: {}".format(e))
