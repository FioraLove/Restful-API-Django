# -*- coding:utf-8 -*-
from rest_framework import serializers
from . import models


class New_Category_Serializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=32)
    class Meta:
        model = models.Category
        # field表示展示的字段
        # fields = ['id', 'title', 'summary', 'content', 'category']
        # 展示所有的字段
        fields = "__all__"
        depth = 1  # 此字段表示查看嵌套几层的数据，不建议太大，性能损耗


class ArticleSerializer(serializers.ModelSerializer):
    category_txt = serializers.CharField(source='category.name', required=False)

    # x1 = serializers.SerializerMethodField()

    # status_txt = serializers.CharField(source='get_status_display', required=False)
    #
    # x2 = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        # fields = "__all__"
        fields = ['id', 'title', 'summary', 'content', 'category', 'category_txt']
        depth = 2

    # def get_x1(self, obj):
    #     return obj.category.name

    # def get_x2(self, obj):
    #     return obj.get_status_display()


# 分页序列化方式一
class PageArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = "__all__"


# 分页序列化方式二
class PageArticleSerializer1(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = "__all__"


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


# 用户注册序列化
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        depth = 1


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