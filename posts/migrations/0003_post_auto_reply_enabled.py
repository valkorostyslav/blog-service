# Generated by Django 5.1.2 on 2024-10-21 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_is_blocked_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='auto_reply_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
