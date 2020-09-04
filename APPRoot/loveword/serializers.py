# -*- coding:utf-8 -*-
from rest_framework import serializers
from . import models


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


# 漫画章节表
class ComicChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comic_chapter
        fields = "__all__"
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