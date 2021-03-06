# Generated by Django 2.2.1 on 2020-08-24 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loveword', '0007_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('sid', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='作品id')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('cover', models.CharField(max_length=100, verbose_name='封面')),
                ('judge', models.CharField(max_length=10, verbose_name='评分')),
                ('category', models.CharField(choices=[(1, '冒险热血'), (2, '武侠格斗'), (3, '科幻魔幻'), (4, '侦探推理'), (5, '耽美爱情'), (6, '生活漫画')], default=1, max_length=5, verbose_name='分类')),
                ('update', models.CharField(max_length=100, verbose_name='更新时间')),
                ('update_content', models.CharField(max_length=100, verbose_name='最近更新')),
            ],
        ),
    ]
