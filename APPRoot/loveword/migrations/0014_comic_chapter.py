# Generated by Django 2.2.1 on 2020-08-25 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loveword', '0013_auto_20200824_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comic_chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=10, verbose_name='漫画作品ID')),
                ('cid', models.CharField(max_length=10, verbose_name='章节ID')),
                ('chapter_title', models.CharField(max_length=100, verbose_name='章节标题')),
                ('chapter_number', models.CharField(max_length=10, verbose_name='章节编号')),
                ('images_url', models.TextField(verbose_name='图片url')),
            ],
        ),
    ]
