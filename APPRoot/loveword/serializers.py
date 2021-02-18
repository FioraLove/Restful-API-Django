# -*- coding:utf-8 -*-
from rest_framework import serializers
from . import models


class BilibiliIndex(serializers.ModelSerializer):
    """
    bilibili-个人主页
    """

    class Meta:
        model = models.Bilibili
        fields = "__all__"
        depth = 1


# 嘴臭生成器序列化
class NmslAndNdslSerializer(serializers.ModelSerializer):
    # level = serializers.SerializerMethodField()
    class Meta:
        model = models.Nmsl
        fields = "__all__"
        depth = 1
    # 获取models模型中choices的值,参考文章https://blog.csdn.net/qq_41854273/article/details/84987899
    # def get_level(self, obj):
    #     return obj.get_level_display()


# 漫画主页
class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comic
        fields = "__all__"
        depth = 1


# 漫画作者表
class ComicAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comic_author
        fields = "__all__"
        depth = 1


# 漫画具体章节表
class ComicChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comic_chapter
        fields = "__all__"
        depth = 1


# 漫画章节目录大全序列化
class ComicChapterCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comic_chapter
        fields = ["chapter_title", "cid", "chapter_number", 'uid']
        depth = 1


# 加密视频序列化
class AVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AVideo
        fields = "__all__"
        depth = 1


# 加密视频集数播放地址序列化
class AVideoChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AVideo_chapter
        fields = "__all__"
        depth = 1


# 加密图片地址序列化
class APictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.APicture
        fields = "__all__"
        depth = 1


# 留言-回复序列化
class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comments
        fields = "__all__"
        depth = 1


# 社会小伙经典语录序列化
class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quotation
        fields = "__all__"
        depth = 1
