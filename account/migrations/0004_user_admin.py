# Generated by Django 3.0.8 on 2020-12-02 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_confirmstring'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]