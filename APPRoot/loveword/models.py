from django.conf import settings
from django.db import models


# Create your models here.
# 嘴臭生成器模块
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


# 漫画作品大全主页
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
    update = models.CharField(verbose_name="更新时间", max_length=100)
    update_content = models.CharField(verbose_name="最近更新", max_length=100)
    objects = models.Manager()


# 漫画作者相关信息
class Comic_author(models.Model):
    """
    漫画作者明细表
    """
    uid = models.CharField(verbose_name="漫画作品ID", max_length=10, primary_key=True)
    author = models.CharField(verbose_name="作者名", max_length=50)
    title = models.CharField(verbose_name="标题", max_length=50)
    location = models.CharField(verbose_name="分类", max_length=50)
    copyright = models.CharField(verbose_name="版权", max_length=5)  # 版权0(无版权)或1
    state = models.CharField(verbose_name="状态", max_length=5)  # 更新状态：1表示连载中，0表示完结
    content = models.TextField(verbose_name="简介")
    objects = models.Manager()


# 漫画具体章节
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


# 隐私加密视频大全主页
class AVideo(models.Model):
    """
    加密视频模型
    """
    vid = models.CharField(verbose_name="视频作品ID", max_length=10)
    title = models.CharField(verbose_name="标题", max_length=200)
    pic = models.CharField(verbose_name="封面", max_length=200)
    judge = models.FloatField(verbose_name="评分")
    quality = models.CharField(verbose_name="画质", max_length=50, blank=True, null=True, default="")
    update = models.CharField(verbose_name="更新时间", max_length=50)
    objects = models.Manager()


# 隐私加密视频明细
class AVideo_chapter(models.Model):
    """
    加密视频章节
    """
    vid = models.CharField(verbose_name="视频作品ID", max_length=10)
    images_url = models.TextField(verbose_name="图片url")
    objects = models.Manager()


# 隐私加密图片
class APicture(models.Model):
    """
    加密隐私图片
    """
    items = (
        (1, "巨乳"),
        (2, "大公鸡"),
        (3, "写真"),
        (4, "口交"),
        (5, "无码"),
        (6, "制服"),
        (7, "主播"),
    )
    title = models.CharField(verbose_name="图片标题", max_length=250, blank=True)
    images_url = models.CharField(verbose_name="图片url", max_length=250, blank=True)
    category = models.CharField(verbose_name="分类", choices=items, max_length=5, default=1)
    objects = models.Manager()


class Comments(models.Model):
    """
    留言模块：评论留言
    """
    ip = models.CharField(verbose_name="留言ip地址", max_length=20, blank=True, null=True)
    uid = models.CharField(verbose_name="用户id", max_length=20, blank=True, null=True)
    location = models.CharField(verbose_name="用户地址", max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name="邮箱", max_length=50, blank=True, )
    contents = models.CharField(verbose_name="留言内容", max_length=240, blank=True, null=True)
    reply = models.CharField(verbose_name="回复", max_length=240, blank=True, null=True)
    update = models.DateField(verbose_name="创建时间", auto_now_add=True)
    objects = models.Manager()


class Bilibili(models.Model):
    """
    bilibili主页视频模块
    """
    bvid = models.CharField(verbose_name="bv号", max_length=20, primary_key=True)
    comment = models.IntegerField(verbose_name="评论数", blank=True, null=True, default=0)
    created = models.CharField(verbose_name="创建时间", max_length=20, blank=True, null=True)
    pic = models.CharField(verbose_name="图片地址", max_length=100, blank=True, null=True)
    title = models.CharField(verbose_name="标题", max_length=100, blank=True, null=True)
    length = models.CharField(verbose_name="视频长度", max_length=10, blank=True, null=True)
    play = models.IntegerField(verbose_name="播放量", blank=True, null=True, default=0)
    ts = models.IntegerField(verbose_name="时间戳", blank=True, null=True)
    objects = models.Manager()


class Quotation(models.Model):
    """
    精神小伙经典语录
        1: 社会精神小伙经典语录
    """
    category = models.IntegerField(verbose_name="类型", blank=True, null=True, default=1)
    content = models.CharField(verbose_name="文本内容", max_length=255, blank=False, default="社会经典语录")
    objects = models.Manager()
