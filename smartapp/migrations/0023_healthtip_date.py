# Generated by Django 3.2.4 on 2021-10-27 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartapp', '0022_auto_20211027_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthtip',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
