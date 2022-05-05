# Generated by Django 3.2.6 on 2022-04-13 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0014_auto_20220413_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='name',
            field=models.SlugField(help_text='Internal name of the experiment; Only letters, numbers, underscores or hyphens.', verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='title',
            field=models.CharField(help_text='Title of the experiment; visible to participants.', max_length=50, verbose_name='title'),
        ),
    ]