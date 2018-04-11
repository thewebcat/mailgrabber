import time
from django.core.mail import send_mail
from django.test import TestCase, override_settings

from email_settings.models import EmailSetting
from receiver.receiver import email_getter, create_index, insert_to_es, delete_index
from elasticsearch import Elasticsearch, NotFoundError


@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
@override_settings(USE_DJANGO_SEND_MAIL=True)
@override_settings(SERVER_EMAIL='test.constantin@yandex.ru')
@override_settings(DEFAULT_FROM_EMAIL='test.constantin@yandex.ru')
@override_settings(EMAIL_HOST='smtp.yandex.ru')
@override_settings(EMAIL_HOST_USER='test.constantin@yandex.ru')
@override_settings(EMAIL_HOST_PASSWORD='u7lAG8Nq8i')
@override_settings(EMAIL_PORT=587)
@override_settings(EMAIL_USE_TLS=True)
class EmailTest(TestCase):
    emails = []
    es = Elasticsearch()

    def setUp(self):
        EmailSetting.objects.create(name='test', active=True, email_user='test.constantin@yandex.ru',
                                    email_password='u7lAG8Nq8i', email_port='993', email_host='imap.yandex.ru',
                                    tag='[TEST_ALERT]')


    def test_01_send_email(self):
        res = send_mail(
            '[TEST_ALERT] Тестовое тема сообщения',
            'Тествое сообщение с тестовой информацией для размышения.',
            'test.constantin@yandex.ru',
            ['test.constantin@yandex.ru'],
            fail_silently=False,
        )
        self.assertEquals(res, 1)

    def test_02_pause(self):
        time.sleep(10)

    def test_03_get_emails(self):
        email_setting = EmailSetting.objects.last()
        self.assertEqual(email_setting.id, 1)
        emails_count = 0
        for item in email_getter():
            self.assertIsInstance(item, dict)
            self.assertEqual(item['subject'].replace("\r\n", ""), '[TEST_ALERT] Тестовое тема сообщения')
            self.assertEqual(item['msg'].replace("\r\n", ""), 'Тествое сообщение с тестовой информацией для размышения.')
            self.emails.append(item)
            emails_count += 1
        self.assertEqual(emails_count, 1)

    def test_04_create_es_index(self):
        create_index('test_index')
        self.assertIsInstance(self.es.indices.get('test_index'), dict)

    def test_05_insert_emails(self):
        def template(query):
            return {
                "query": {
                    "bool": {"should": [
                        {"simple_query_string": {
                            "query": query,
                            "fields": ["subject", "msg"]
                        }}
                    ]}
                },
                "highlight": {
                    "pre_tags": ["<strong>"],
                    "post_tags": ["</strong>"],
                    "fields": {
                        "subject": {"fragment_size": 150, "number_of_fragments": 1},
                        "msg": {"fragment_size": 150, "number_of_fragments": 1}
                    }
                }
            }
        insert_to_es(self.emails, index='test_index')
        time.sleep(3)
        hits_count = self.es.search(index='test_index', doc_type='mail', body=template('тестовое'))['hits']['total']
        self.assertEqual(hits_count, 1)
        hits_count = self.es.search(index='test_index', doc_type='mail', body=template('тестовый'))['hits']['total']
        self.assertEqual(hits_count, 1)
        hits_count = self.es.search(index='test_index', doc_type='mail', body=template('сообщение'))['hits']['total']
        self.assertEqual(hits_count, 1)
        hits_count = self.es.search(index='test_index', doc_type='mail', body=template('сообщения'))['hits']['total']
        self.assertEqual(hits_count, 1)

    def test_06_delete_es_index(self):
        delete_index('test_index')
        with self.assertRaises(NotFoundError):
            self.es.indices.get('test_index')


