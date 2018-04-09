from django.db import models


class EmailSetting(models.Model):
    name = models.CharField(verbose_name='E-mail сервис', max_length=100)
    active = models.BooleanField(verbose_name='Активный', default=False)
    email_user = models.CharField(verbose_name='Пользователь', max_length=100)
    email_password = models.CharField(verbose_name='Пароль', max_length=20)
    email_host = models.CharField(verbose_name='Хост', max_length=50)
    email_port = models.CharField(verbose_name='Порт', max_length=10)
    tag = models.CharField(verbose_name='Тэг поиска', max_length=100)

    def __str__(self):
        return self.name
