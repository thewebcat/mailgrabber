from mailgrabber.celery import app
from receiver.receiver import email_getter, insert_to_es


@app.task(name='get_email')
def emails():
    insert_to_es(email_getter())