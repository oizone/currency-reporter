from google_currency import convert
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


kzt_limit=0.0023
rub_limit=0.013
mxn_limit=0.046

kzt=float(json.loads(convert('kzt', 'eur', 1)).get('amount'))
rub=float(json.loads(convert('rub', 'eur', 1)).get('amount'))
mxn=float(json.loads(convert('mxn', 'eur', 1)).get('amount'))

message="Results on currency rates:\r\n"


if kzt > kzt_limit:
    print("kzt ok")
else:
    print("kzt not")

if mxn > mxn_limit:
    print("mxn ok")
else:
    print("mxn not")

if rub > rub_limit:
    print("rub ok")
else:
    print("rub not")

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    #server.SMTP_SSL()
    server.starttls()
    # ...send emails
except:
    print('Something went wrong...')

message_template = read_template('template')

msg = MIMEMultipart()
message = message_template.substitute(KZT=kzt)
msg['From']="currency@oizone.net"
msg['To']="oizone@oizone.net"
msg['Subject']="This is KZT"
msg.attach(MIMEText(message, 'plain'))
server.send_message(msg)
del msg

#s = smtplib.SMTP(host='your_host_address_here', port=your_port_here)
