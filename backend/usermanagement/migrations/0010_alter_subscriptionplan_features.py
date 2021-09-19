# Generated by Django 3.2.5 on 2021-07-29 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0009_auto_20210728_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='features',
            field=models.JSONField(verbose_name='The plan\'s features as a list of dictionaries e.g. ["This is a feature", "This is another feature"]'),
        ),
    ]