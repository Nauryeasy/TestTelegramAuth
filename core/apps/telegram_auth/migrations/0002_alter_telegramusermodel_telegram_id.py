# Generated by Django 5.1.4 on 2024-12-04 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramusermodel',
            name='telegram_id',
            field=models.CharField(unique=True),
        ),
    ]
