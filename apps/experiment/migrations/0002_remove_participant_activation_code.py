# Generated by Django 3.2.6 on 2021-10-08 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='activation_code',
        ),
    ]