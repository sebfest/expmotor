# Generated by Django 3.2.6 on 2021-09-26 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0007_auto_20210926_2014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participant',
            old_name='linkcode',
            new_name='activation_code',
        ),
        migrations.RenameField(
            model_name='participant',
            old_name='cellphone',
            new_name='phone',
        ),
    ]
