# Generated by Django 3.2.10 on 2022-03-06 19:46

from django.db import migrations, models
import django.db.models.deletion

import environ
from django.contrib.auth import get_user_model

env = environ.Env()


def create_data(apps, schema_editor):
    """Creates admin user"""
    User = get_user_model()
    user = User.objects.create_superuser(
        email=env("ADMIN_EMAIL"),
        auth_provider_sub=env("ADMIN_EMAIL"),
        is_active=True,
        first_name="Super",
        last_name="Admin",
    )
    user.save()
    user.set_password(env("ADMIN_PASSWORD"))
    user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("djstripe", "0008_2_5"),
        ("usermanagement", "0002_auto_20220227_1921"),
    ]

    operations = [
        migrations.AddField(
            model_name="myuser",
            name="stripe_customer",
            field=models.OneToOneField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="djstripe.customer",
            ),
        ),
        migrations.DeleteModel(
            name="Workspace",
        ),
        migrations.RunPython(create_data),
    ]