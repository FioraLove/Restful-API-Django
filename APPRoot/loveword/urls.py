# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.urls import path, re_path
from . import views  # 导入views文件中的视图函数(标准写法)

urlpatterns = [
    # 获取一条文章的信息
    re_path(r'^drf/category/$', views.DrfCategoryView.as_view()),
    re_path(r'^drf/category/(?P<pk>\d+)/$', views.DrfCategoryView.as_view()),

    # 序列化
    re_path(r'^new/category/$', views.NewCategoryView.as_view()),
    re_path(r'^new/category/(?P<pk>\d+)/$', views.NewCategoryView.as_view()),

    # get获取列表
    # post增加数据
    re_path(r'^drf/article/$', views.ArticleView.as_view()),
    re_path(r'^drf/article/(?P<pk>\d+)/$', views.ArticleView.as_view()),

    # 分页查询一：查询字符串形式为： page/view/article/?page=2
    re_path(r'^page/view/article/$', views.PageViewArticleView.as_view()),
    # 分页查询二：查询字符串形式为： page/article/?offset=0&limit=3
    re_path(r'^page/article/$', views.PageArticleView.as_view()),

    # 嘴臭生成器
    re_path(r'^ndsl/(?P<pk>\d+)/', views.Nmsl8.as_view()),

    # 用户认证
    re_path('login', views.LoginView.as_view()),

    re_path('order', views.OrderView.as_view()),
    re_path(r'^user$', views.UserView.as_view()),

    # 咪咕歌曲下载
    re_path(r'^music$', views.MiGu.as_view()),

    # 视频解析api
    path("api/video/parse/", views.VideoParse.as_view()),

    # 哔哩哔哩个人主页
    path("bilibili/", views.BIli.as_view()),

    # 漫画作品api
    path("api/comic/", views.Comics.as_view()),

    # 漫画作者api
    path("api/comic/author/", views.Comic_Author.as_view()),

    # 漫画章节api
    path("api/comic/chapter/", views.Comic_chapters.as_view()),
]
