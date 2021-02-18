# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.urls import path, re_path
from . import views  # 导入views文件中的视图函数(标准写法)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # 嘴臭生成器
    re_path(r'^ndsl/(?P<pk>\d+)/', views.Nmsl8.as_view()),

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

    # Token认证，通过输入默认的系统表的auth_user用户表里的账号密码来获取token
    re_path(r"^api/secret/token-auth/", obtain_auth_token),

    # 加密视频
    path("api/secret/video/", views.AVideos.as_view()),

    # 加密视频章节
    path("api/secret/video/chapter/", views.AVideoChapters.as_view()),

    # 加密隐私图片
    path("api/secret/picture/", views.AImages.as_view()),

    # 留言，回复api
    path("api/comments/", views.Comments_Reply.as_view()),

    # 跨域文件下载api
    # path("api/download/", views.FileDownload, name="download"),
    path("api/download/", views.FileDownload.as_view()),

    # 社会经典语录api
    path("api/yulu", views.Quotations.as_view()),
]
