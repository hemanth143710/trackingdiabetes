# Generated by Django 4.2 on 2023-04-30 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_user_is_security_question_required'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_security_question_required',
        ),
    ]
