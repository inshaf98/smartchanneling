# Generated by Django 3.2.4 on 2021-10-27 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartapp', '0021_alter_consult_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthTipCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='healthtip',
            name='image',
            field=models.FileField(null=True, upload_to='newsImages/%y%m%d/'),
        ),
        migrations.AddField(
            model_name='healthtip',
            name='title',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
