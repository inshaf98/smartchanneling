# Generated by Django 3.2.4 on 2021-11-14 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartapp', '0026_auto_20211114_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consult',
            name='bmi',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
