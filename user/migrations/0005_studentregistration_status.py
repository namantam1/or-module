# Generated by Django 3.2.7 on 2021-09-18 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_specialization_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentregistration',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('rejected', 'rejected'), ('accepted', 'accepted')], default='pending', max_length=20),
        ),
    ]