# Generated by Django 3.0.7 on 2020-06-09 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_auto_20200609_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='following',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
