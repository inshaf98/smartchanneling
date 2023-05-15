# Generated by Django 3.2.4 on 2021-10-25 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smartapp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smartapp', '0017_alter_identification_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=300, null=True)),
                ('age', models.IntegerField(null=True)),
                ('weight', models.CharField(max_length=300, null=True)),
                ('symptoms', models.TextField(null=True)),
                ('allergiesEms', models.TextField(blank=True, null=True)),
                ('date', models.DateField(null=True)),
                ('advice', models.TextField(null=True)),
                ('img1', models.ImageField(blank=True, null=True, upload_to=smartapp.models.additional_directory_path)),
                ('img2', models.ImageField(blank=True, null=True, upload_to=smartapp.models.additional_directory_path)),
                ('img3', models.ImageField(blank=True, null=True, upload_to=smartapp.models.additional_directory_path)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='smartapp.doctor')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Identification',
        ),
    ]
