# Generated by Django 3.1.5 on 2021-07-19 20:07

from django.db import migrations
import usermanagement.models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0002_organisation'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', usermanagement.models.UserManager()),
            ],
        ),
    ]