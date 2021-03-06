# Generated by Django 3.2.6 on 2021-10-18 22:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0005_alter_experiment_final_instructions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='final_instructions',
            field=models.TextField(default='We confirm your participation in the experiment.\n    \nYou are registered for participation on {{ date }}, {{ time }} at {{ place }}.\n\nThe research group is grateful for your contribution,\nand it is important to us that you take part. \n\nShould you need to cancel, or get in touch with us for\nsome other reason, you can do so by email to {{ email }},\nor contact {{ manager }} by phone: {{ phone }}. \n\nOn behalf of the research group,\n{{ manager| title }}.\n', help_text='Message in email sent after confirmation of email address.', verbose_name='instructions mail'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='phone',
            field=models.CharField(help_text='Phone number participants can contact.', max_length=8, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '12345678'.", regex='^\\d{8}$')], verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='registration_help',
            field=models.TextField(default='<p> This page lets you register for the experiment.</p>\n<p> You need to tick off the session you would like to take part in.</p>\n', help_text='This text will meet participants when registering for participation.', verbose_name='registration instructions'),
        ),
        migrations.AlterField(
            model_name='session',
            name='max_subjects',
            field=models.PositiveIntegerField(help_text='The maximal number of participants that can register.', validators=[django.core.validators.MinValueValidator(limit_value=1, message='You must provide space for at least one subject.')], verbose_name='number of subjects.'),
        ),
    ]
