# Generated by Django 2.2.16 on 2022-06-15 11:38

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220601_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
            ],
            options={
                'verbose_name': 'подписка',
                'verbose_name_plural': 'подписки',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]