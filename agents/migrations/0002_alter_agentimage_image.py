# Generated by Django 4.2.18 on 2025-03-02 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentimage',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
