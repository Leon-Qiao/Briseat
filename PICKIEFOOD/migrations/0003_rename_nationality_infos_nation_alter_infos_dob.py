# Generated by Django 4.1 on 2024-02-26 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PICKIEFOOD', '0002_infos_delete_choice_delete_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='infos',
            old_name='nationality',
            new_name='nation',
        ),
        migrations.AlterField(
            model_name='infos',
            name='dob',
            field=models.CharField(max_length=200),
        ),
    ]
