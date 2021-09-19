# Generated by Django 3.2.7 on 2021-09-18 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210918_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentregistration',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to='files', verbose_name='URL of document uploaded'),
        ),
        migrations.AlterField(
            model_name='studentregistration',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]