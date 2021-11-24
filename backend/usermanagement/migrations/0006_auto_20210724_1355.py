# Generated by Django 3.1.5 on 2021-07-24 11:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usermanagement", "0005_auto_20210723_1840"),
    ]

    operations = [
        migrations.AddField(
            model_name="organisation",
            name="admins",
            field=models.ManyToManyField(
                related_name="admins",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Organisation Admins",
            ),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="members",
            field=models.ManyToManyField(
                related_name="members",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Organisation Members",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                verbose_name="active",
            ),
        ),
    ]
