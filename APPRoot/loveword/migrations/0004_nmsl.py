# Generated by Django 2.2.1 on 2020-07-31 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loveword', '0003_auto_20200721_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nmsl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(1, '莲花模式'), (2, '仙人模式'), (3, '气急败坏'), (4, 'NMSL')], default=1, verbose_name='嘴臭限度')),
                ('content', models.TextField(verbose_name='嘴臭内容')),
            ],
        ),
    ]
