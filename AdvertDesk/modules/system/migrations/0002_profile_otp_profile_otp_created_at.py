# Generated by Django 5.1 on 2024-08-29 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='otp_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
