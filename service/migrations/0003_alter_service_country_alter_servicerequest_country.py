# Generated by Django 4.2.18 on 2025-02-06 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_service_country_servicerequest_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
