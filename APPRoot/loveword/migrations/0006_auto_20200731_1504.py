# Generated by Django 2.2.1 on 2020-07-31 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loveword', '0005_nmsl_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nmsl',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='嘴臭时间'),
        ),
    ]
