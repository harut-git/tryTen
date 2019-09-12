import os
import time
from multiprocessing import cpu_count, freeze_support
from multiprocessing.pool import Pool

from lorem import text, sentence
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import markovify  # Markov Chain Generator
# Any results you write to the current directory are saved as output.
from smtp_send.Utils.SmtpSender import send_message, sendReply

names = [None, 'Andrew McCartney', 'Mike Ross', 'Donna Paulsen', 'Daniel Whitehall']
print('---------------------------', os.getcwd())
# subjects = ['I was right - and that’s not good for you', '13 email marketing trends you must know', 'Before you write another blog post, read this', 'We’re starting in 5 HOURS', 'It’s time to rethink Black Friday', 'How to Google-proof your mobile site in 2017', ]
inp = pd.read_csv('smtp_send/Utils/abcnews-date-text.csv')
inp.head(3)
text_model = markovify.NewlineText(inp.headline_text, state_size=2)
# for i in range(5):
#     print(text_model.make_sentence())

accs = {
    'smithjjhn@gmail.com': ('John Smith', "ZeroApp#123"),
    'kleithkevin@gmail.com': ('Kevin Kleith', "ZeroApp#123"),
    'test1zeroapp@gmail.com': ('Andrew McCartney', "Test123321"),
    'test2zeroapp@gmail.com': ('Mike Ross', "Test123321"),
    'test3zeroapp@gmail.com': ('Donna Paulsen', "Test123321"),
    'test4zeroapp@gmail.com': ('Daniel Whitehall', "Test123321")
}

jobs = ['kleithkevin@gmail.com', 'smithjjhn@gmail.com', 'test1zeroapp@gmail.com', 'test2zeroapp@gmail.com',
        'test3zeroapp@gmail.com', 'test4zeroapp@gmail.com']


def prepare_data(test_account_id, email):
    sample = {
        "host": "smtp.gmail.com",
        "port": 465,
        "username": test_account_id,
        "password": accs[test_account_id][1],
        "subject": text_model.make_sentence(),
        "to": email,
        "from": accs[test_account_id][0],
        "text": text()
    }
    send_message(
        host=sample['host'],
        port=sample['port'],
        username=sample['username'],
        password=sample['password'],
        subject=sample['subject'],
        msg_to=sample['to'],
        msg_from=sample['from'],
        msg_text=sample['text']

    )


def prepare_conversation_data(test_account_id, email, username, pswd, threads_count):
    sample = {
        "host": "smtp.gmail.com",
        "port": 465,
        "username": test_account_id,
        "password": accs[test_account_id][1],
        "subject": text_model.make_sentence(),
        "to": email,
        "from": accs[test_account_id][0],
        "text": text()
    }
    msg_id = send_message(
        host=sample['host'],
        port=sample['port'],
        username=sample['username'],
        password=sample['password'],
        subject=sample['subject'],
        msg_to=sample['to'],
        msg_from=sample['from'],
        msg_text=sample['text']

    )
    sample_reply = {"host": "smtp.office365.com", "username": username, "password": pswd,
                    "subject": sample['subject'], "to": email, "from": accs[test_account_id][0],
                    "text": text(), 'In-Reply-To': msg_id}
    for _ in range(threads_count):
        sendReply(host=sample_reply['host'],
                  port=587,
                  username=sample_reply['username'],
                  password=sample_reply['password'],
                  subject=sample_reply['subject'],
                  msg_to=sample_reply['to'],
                  msg_from=sample_reply['from'],
                  msg_text=sample_reply['text'],
                  msg_id=sample_reply['In-Reply-To']
                  )
        time.sleep(10)
        sendReply(host=sample['host'],
                  port=465,
                  username=sample['username'],
                  password=sample['password'],
                  subject=sample['subject'],
                  msg_to=sample['to'],
                  msg_from=sample['from'],
                  msg_text=sample['text'],
                  msg_id=sample_reply['In-Reply-To']
                  )
