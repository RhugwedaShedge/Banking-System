# Generated by Django 3.1.4 on 2021-11-30 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0008_auto_20211130_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbankaccount',
            name='mobile_no',
            field=models.CharField(max_length=11),
        ),
    ]