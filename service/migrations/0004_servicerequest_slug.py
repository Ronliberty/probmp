# Generated by Django 4.2.18 on 2025-02-08 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_service_country_alter_servicerequest_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequest',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
