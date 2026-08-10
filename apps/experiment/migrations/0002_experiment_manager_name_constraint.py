from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='experiment',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='experiment',
            constraint=models.UniqueConstraint(
                fields=('manager', 'name'),
                name='experiment_manager_name_unique',
            ),
        ),
    ]
