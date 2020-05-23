from google_currency import convert
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib
import time

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


kzt_limit=0.002314
mxn_limit=0.046548
rub_limit=0.013796
pln_limit=0.23


while True:
    try:
        kzt=float(json.loads(convert('kzt', 'eur', 100000)).get('amount'))/100000
    except:
        kzt=0
    try:
        mxn=float(json.loads(convert('mxn', 'eur', 100000)).get('amount'))/100000
    except:
        mxn=0
    try:
        pln=float(json.loads(convert('pln', 'eur', 100000)).get('amount'))/100000
    except:
        pln=0
    try:
        rub=float(json.loads(convert('rub', 'eur', 100000)).get('amount'))/100000
    except:
        rub=0

    kzt_diff=round((kzt-kzt_limit)/kzt_limit*100,2)
    mxn_diff=round((mxn-mxn_limit)/mxn_limit*100,2)
    pln_diff=round((pln-pln_limit)/pln_limit*100,2)
    rub_diff=round((rub-rub_limit)/rub_limit*100,2)

    limit=0
    if kzt > kzt_limit:
        limit=1
        print("kzt ok")
    else:
        print("kzt not")

    if mxn > mxn_limit:
        limit=1
        print("mxn ok")
    else:
        print("mxn not")

    if rub > rub_limit:
        limit=1
        print("rub ok")
    else:
        print("rub not")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('smtp@oizone.net','sc9Y58pfb49h1OX')
        # ...send emails
    except:
        print('Something went wrong...')

    message_template = read_template('template')

    msg = MIMEMultipart()
    message = message_template.substitute(KZT=kzt,MXN=mxn,RUB=rub,KZT_LIMIT=kzt_limit,MXN_LIMIT=mxn_limit,RUB_LIMIT=rub_limit,KZT_DIFF=kzt_diff,MXN_DIFF=mxn_diff,RUB_DIFF=rub_diff,PLN=pln,PLN_LIMIT=pln_limit,PLN_DIFF=pln_diff)
    msg['From']="currency@oizone.net"
    msg['To']="oizone@oizone.net"
    msg['Subject']="Currency report"
    msg.attach(MIMEText(message, 'plain'))
    server.send_message(msg)
    del msg
    time.sleep(60)

#s = smtplib.SMTP(host='your_host_address_here', port=your_port_here)
