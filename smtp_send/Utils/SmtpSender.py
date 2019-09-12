import smtplib
from email.mime.text import MIMEText
from email.utils import make_msgid


def send_message(host, port, username, password, subject, msg_to, msg_from, msg_text):
    subject = subject
    message = msg_text
    send_from = msg_from
    msg = MIMEText(message, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = msg_to
    msg['Message-ID'] = make_msgid()
    send_to = [msg_to]

    smtp_server = host
    smtp_port = port
    user_name = username
    password = password
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.ehlo()
        server.login(user_name, password)
        server.sendmail(send_from, send_to, msg.as_string())
        print("Email sent!")
        server.quit()
        return msg['Message-ID']
    except Exception as e:
        print("Something went wrong")
        print(e)


def send_internal_message(host, username, password, subject, msg_to, msg_from, msg_text, smtp_port=465):
    subject = subject
    message = msg_text
    send_from = msg_from
    msg = MIMEText(message, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = msg_to
    msg['Message-ID'] = make_msgid()
    send_to = [msg_to]

    smtp_server = host
    user_name = username
    password = password
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.ehlo()
        server.login(user_name, password)
        server.sendmail(send_from, send_to, msg.as_string())
        print("Email sent!")
        server.quit()
        return msg['Message-ID']
    except Exception as e:
        print("Something went wrong")
        print(e)


def sendReply(host, port, username, password, subject, msg_to, msg_from, msg_text, msg_id):
    to_email = msg_to
    username = username
    message = msg_text
    msg = MIMEText(message, 'html', 'utf-8')
    msg['From'] = msg_from
    msg['To'] = msg_to
    msg['Subject'] = "RE: " + subject
    msg['In-Reply-To'] = msg_id
    if port == 465:
        server = smtplib.SMTP_SSL(host, port)
    else:
        server = smtplib.SMTP(host, port)
        server.starttls()
    try:

        # identify ourselves, prompting server for supported features
        server.ehlo()
        server.login(username, password)
        server.sendmail(username, [to_email], msg.as_string())
        print("Reply sent!")
    finally:
        server.quit()
