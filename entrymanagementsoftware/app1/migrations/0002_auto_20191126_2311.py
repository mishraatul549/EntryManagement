# Generated by Django 2.1.7 on 2019-11-26 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='checkInTime',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='checkOutTime',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
