# Generated by Django 2.2 on 2019-11-19 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.IntegerField(blank=True)),
                ('status', models.SmallIntegerField(blank=True, choices=[(1, 'Жасалуда'), (2, 'Дайын')], default=1)),
                ('unit', models.SmallIntegerField(blank=True)),
                ('display', models.SmallIntegerField(blank=True, choices=[(1, 'display'), (2, 'none')], default=1)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Product')),
            ],
        ),
    ]
