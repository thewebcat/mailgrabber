import base64
import email
import email.utils
import datetime
import quopri
import time
from imaplib import IMAP4_SSL
from email.header import decode_header
from elasticsearch import Elasticsearch

from email_settings.models import EmailSetting

es = Elasticsearch()


def delete_index(index='mailer'):
    es.indices.delete(index=index)


def create_index(index='mailer'):
    es.indices.create(
        index=index,
        body={
            "settings": {
                "analysis": {
                    "filter": {
                        "ru_stop": {
                            "type": "stop",
                            "stopwords": "_russian_"
                        },
                        "ru_stemmer": {
                            "type": "stemmer",
                            "language": "russian"
                        }
                    },
                    "analyzer": {
                        "default": {
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "ru_stop",
                                "ru_stemmer"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "mail": {
                    "properties": {
                        "subject": {
                            "type": "text"
                        },
                        "date": {
                            "type": "date",
                            "index": "false"
                        },
                        "from": {
                            "type": "text",
                            "index": "false"
                        },
                        "msg": {
                            "type": "text"
                        }
                    }
                }
            }
        },
        ignore=400
    )


def get_charset(text):
    text = text.split()
    try:
        if len(text) > 1:
            return text[1].split('=')[1]
        else:
            return text[0].split('=')[1]
    except IndexError:
        return None


def email_getter():
    for item in EmailSetting.objects.filter(active=True):
        conn = IMAP4_SSL(host=item.email_host, port=item.email_port)
        conn.login(user=item.email_user, password=item.email_password)
        status, msgs = conn.select('INBOX')
        assert status == 'OK', 'Connection error {}'.format(msgs)

        # убрать отладочный email
        _, data = conn.search(None, '(UNSEEN)', 'SUBJECT "{}"'.format(item.tag))

        for i in data[0].split():
            _, message_data = conn.fetch(i, '(RFC822)')
            msg = email.message_from_bytes(message_data[0][1])
            content_transfer_encoding = msg["Content-Transfer-Encoding"]
            content_type = msg["Content-Type"]
            message = dict()
            message['id'] = '{0}-{1}'.format(str(item.id), i.decode("utf-8"))
            subject_text = decode_header(msg['Subject'])[0][0]
            subject_coding = decode_header(msg['Subject'])[0][1]
            if subject_coding:
                subject = subject_text.decode(subject_coding)
            else:
                subject = msg['Subject']
            message['subject'] = subject
            message['from'] = msg['From']
            message['date'] = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(msg['Date'])))

            payload = msg.get_payload()
            if content_transfer_encoding == "base64":
                payload = base64.b64decode(payload)
            elif content_transfer_encoding == "quoted-printable":
                payload = quopri.decodestring(payload)

            if isinstance(payload, str):
                message['msg'] = payload
            else:
                message['msg'] = payload.decode(get_charset(content_type))

            yield message

        conn.close()
        conn.logout()


def insert_to_es(emails, index='mailer'):
    for item in emails:
        mail_id = item['id']
        del item['id']
        es.index(index=index, doc_type='mail', id=mail_id, body=item)