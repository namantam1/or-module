# Generated by Django 3.2.7 on 2021-09-18 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentregistration',
            name='registration_number',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempts', models.IntegerField(default=3)),
                ('expire_on', models.DateTimeField(default=user.models.get_expire_time)),
                ('value', models.IntegerField(default=user.models.get_otp)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
