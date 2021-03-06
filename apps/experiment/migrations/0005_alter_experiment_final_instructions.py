# Generated by Django 3.2.6 on 2021-10-16 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0004_alter_session_max_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='final_instructions',
            field=models.TextField(default='\nWe confirm your participation in the experiment.\n    \nYou are registered for participation on {{ date }}, {{ time }} at {{ place }}.\n\nThe research group is grateful for your contribution,\nand it is important to us that you take part. \n\nShould you need to cancel, or get in touch with us for\nsome other reason, you can do so by email to {{ manager.email }},\nor contact {{ manager }} by phone: {{ manager.phone }}. \n\nOn behalf of the research group,\n{{ manager| title }}.\n', help_text='Message in email sent after confirmation of email address.', verbose_name='instructions mail'),
        ),
    ]
