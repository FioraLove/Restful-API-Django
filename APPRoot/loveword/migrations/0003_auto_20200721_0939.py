# Generated by Django 2.2.1 on 2020-07-21 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loveword', '0002_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='内容'),
        ),
    ]
