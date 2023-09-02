import requests
import selectorlib
import smtplib, ssl
import logs as logins

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)['tour']

    value1 = extractor.extract(source)['nextTour']
    # return f'{value1} {value}'
    return value


def writeText(text):
    filepath = "data.txt"
    with open(filepath, "a") as file:
        file.write(text + "\n")


def readText():
    filepath = "data.txt"
    with open(filepath, 'r') as fileRead:
        readME = fileRead.read()

    return readME


def send_mail(msg):
    sender = logins.mailMe()
    password = logins.passMe()
    receiver = logins.mailMe()

    context = ssl.create_default_context()
    host = "smtp.gmail.com"
    port = 465
    message = ""
    message = "Subject: Tour Update" \
              + "\n " + "Title: Next Tour:" \
              + "\n " + msg

    message_enc = message.encode("utf-8")

    with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:
        server.login(sender, password)
        server.sendmail(from_addr=sender,to_addrs=receiver,msg=message_enc)

    print("email sent")


if __name__ == "__main__":
    scr = scrape(URL)
    ext = extract(scr)
    readCom = readText()
    print(f'Next Tour: {ext}')

    if ext != "No upcoming tours" and ext not in readCom:
        # print(f'Next Tour: {ext}')
        writeText(ext)
        send_mail(ext)
