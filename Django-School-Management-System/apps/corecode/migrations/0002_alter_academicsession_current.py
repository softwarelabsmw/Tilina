# Generated by Django 4.0.2 on 2022-04-30 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corecode', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicsession',
            name='current',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
