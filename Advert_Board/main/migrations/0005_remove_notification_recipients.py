# Generated by Django 5.0.4 on 2024-04-15 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_verification_code_number_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='recipients',
        ),
    ]
