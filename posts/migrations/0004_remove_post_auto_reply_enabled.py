# Generated by Django 5.1.2 on 2024-10-21 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_auto_reply_enabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='auto_reply_enabled',
        ),
    ]
