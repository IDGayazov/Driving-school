# Generated by Django 5.1.5 on 2025-01-19 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_emailverification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]