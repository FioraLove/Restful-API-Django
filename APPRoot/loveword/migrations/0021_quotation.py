# Generated by Django 2.2.1 on 2021-02-17 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loveword', '0020_bilibili'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='语录内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
    ]
