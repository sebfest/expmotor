# Generated by Django 3.2.13 on 2022-05-19 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0017_auto_20220518_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='qr_code_image',
            field=models.ImageField(blank=True, help_text='Qr_code image with URL to registration site.', upload_to='qr_codes/', verbose_name='qr_code'),
        ),
    ]
