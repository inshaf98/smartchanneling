# Generated by Django 3.2.4 on 2021-10-26 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartapp', '0018_auto_20211025_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consult',
            name='doctor',
            field=models.CharField(max_length=300, null=True),
        ),
    ]