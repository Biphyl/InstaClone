# Generated by Django 3.0.7 on 2020-06-08 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_date']},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='date_created',
            new_name='created_date',
        ),
        migrations.AlterModelTable(
            name='post',
            table='post',
        ),
    ]