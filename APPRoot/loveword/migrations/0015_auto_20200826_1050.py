# Generated by Django 2.2.1 on 2020-08-26 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loveword', '0014_comic_chapter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic_chapter',
            name='chapter_number',
            field=models.IntegerField(max_length=10, verbose_name='章节编号'),
        ),
    ]