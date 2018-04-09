# Generated by Django 2.0.4 on 2018-04-08 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='E-mail сервис')),
                ('active', models.BooleanField(default=False, verbose_name='Активный')),
                ('email_user', models.CharField(max_length=100, verbose_name='Пользователь')),
                ('email_password', models.CharField(max_length=20, verbose_name='Пароль')),
                ('email_host', models.CharField(max_length=50, verbose_name='Хост')),
                ('email_port', models.CharField(max_length=10, verbose_name='Порт')),
                ('tag', models.CharField(max_length=100, verbose_name='Тэг поиска')),
            ],
        ),
    ]