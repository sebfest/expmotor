# Generated by Django 3.2.6 on 2022-03-12 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0010_auto_20220312_2147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['date', 'time']},
        ),
    ]
