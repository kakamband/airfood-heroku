# Generated by Django 2.2 on 2019-12-03 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='user',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='table',
            name='waiter',
            field=models.SmallIntegerField(null=True),
        ),
    ]
