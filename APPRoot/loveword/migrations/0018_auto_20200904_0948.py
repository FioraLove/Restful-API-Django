# Generated by Django 2.2.1 on 2020-09-04 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loveword', '0017_avideo_avideo_chapter'),
    ]

    operations = [
        migrations.CreateModel(
            name='APicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, verbose_name='图片标题')),
                ('images_url', models.CharField(blank=True, max_length=250, verbose_name='图片url')),
                ('category', models.CharField(choices=[(1, '巨乳'), (2, '大公鸡'), (3, '写真'), (4, '口交'), (5, '无码'), (6, '制服'), (7, '主播')], default=1, max_length=5, verbose_name='分类')),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
