# Generated by Django 3.2.4 on 2021-11-14 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartapp', '0025_rename_healthtipcategory_articlecategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='consult',
            name='bmi',
            field=models.DecimalField(decimal_places=0, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='consult',
            name='height',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
