from django.conf import settings
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Category(models.Model):
    """
    文章分类表
    verbose_name 代表别名
    """
    name = models.CharField(verbose_name="分类", max_length=32)
    objects = models.Manager()


class Article(models.Model):
    """
    文章明细表
    """
    title = models.CharField(verbose_name="标题", max_length=32)
    summary = models.CharField(verbose_name="简介", max_length=255)
    content = models.TextField(verbose_name="内容")
    category = models.ForeignKey(verbose_name="分类", to="Category", on_delete=models.CASCADE)
    objects = models.Manager()


# 嘴臭表
class Nmsl(models.Model):
    category_choices = (
        (1, '莲花模式'),
        (2, '仙人模式'),
        (3, '气急败坏'),
        (4, 'NMSL')
    )
    level = models.IntegerField(verbose_name="嘴臭限度", choices=category_choices, default=1)
    content = models.TextField(verbose_name="嘴臭内容", blank=False)
    create_time = models.DateTimeField(verbose_name="嘴臭时间", auto_now_add=True)
    objects = models.Manager()


# 嘴臭用户登录表
class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)
    token = models.CharField(verbose_name="token值", max_length=64, null=True, blank=True)
    objects = models.Manager()


# 漫画主页
class Comic(models.Model):
    """
    漫画章节表
    """
    items = (
        (1, "冒险热血"),
        (2, "武侠格斗"),
        (3, "科幻魔幻"),
        (4, "侦探推理"),
        (5, "耽美爱情"),
        (6, "生活漫画")
    )
    sid = models.CharField(verbose_name="作品id", max_length=10, primary_key=True)
    title = models.CharField(verbose_name="标题", max_length=50)
    cover = models.CharField(verbose_name="封面", max_length=100)
    judge = models.CharField(verbose_name="评分", max_length=10)
    category = models.CharField(verbose_name="分类", choices=items, max_length=5, default=1)
    # copyright = models.IntegerField(verbose_name="版权", max_length=5)    # 版权0或1
    # state = models.IntegerField(verbose_name="状态", max_length=5)    # 更新状态：1表示连载中，0表示完结
    update = models.CharField(verbose_name="更新时间", max_length=100)
    update_content = models.CharField(verbose_name="最近更新", max_length=100)
    objects = models.Manager()


class Comic_author(models.Model):
    """
    漫画作者明细表
    """
    uid = models.CharField(verbose_name="漫画作品ID", max_length=10, primary_key=True)
    author = models.CharField(verbose_name="作者名", max_length=50)
    title = models.CharField(verbose_name="标题", max_length=50)
    location = models.CharField(verbose_name="分类", max_length=50)
    copyright = models.CharField(verbose_name="版权", max_length=5)    # 版权0(无版权)或1
    state = models.CharField(verbose_name="状态", max_length=5)    # 更新状态：1表示连载中，0表示完结
    content = models.TextField(verbose_name="简介")
    objects = models.Manager()


class Comic_chapter(models.Model):
    """
    漫画章节图片的js解密url
    """
    uid = models.CharField(verbose_name="漫画作品ID", max_length=10)
    cid = models.CharField(verbose_name="章节ID", max_length=10)
    chapter_title = models.CharField(verbose_name="章节标题", max_length=100)
    chapter_number = models.IntegerField(verbose_name="章节编号")
    images_url = models.TextField(verbose_name="图片url")
    objects = models.Manager()