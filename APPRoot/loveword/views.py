import uuid
import requests
from django.forms import model_to_dict
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt import authentication

from .models import Category, Article, Nmsl, UserInfo, Comic, Comic_chapter, Comic_author
from .serializers import New_Category_Serializer


# 接口：获取所有文章类型
class DrfCategoryView(APIView):
    def get(self, request, *args, **kwargs):
        """获取所有文章分类/单个文章分类"""
        pk = kwargs.get('pk')
        if not pk:
            # queryset = Article.objects.all().values("category", "content", "id", "summary", "title")
            queryset = Category.objects.all().values('id', 'name')
            data_list = list(queryset)
            return Response(data_list)
        else:
            # category_object = Article.objects.filter(id=pk).first()
            category_object = Category.objects.filter(id=pk).first()
            data = model_to_dict(category_object)
            return Response(data)

    def post(self, request, *args, **kwargs):
        """
        增加一条详细信息
        """
        params = request.data
        if not params:
            return Response({"status": 0, "info": "Failed"})
        else:
            Category.objects.create(**request.data)
            return Response({"status": 1, "info": "Success"})

    def delete(self, request, *args, **kwargs):
        """删除"""
        pk = kwargs.get('pk')
        Category.objects.filter(id=pk).delete()
        return Response({"status": 1, "info": "delete successful"})

    def put(self, request, *args, **kwargs):
        """更新"""
        pk = kwargs.get('pk')
        Category.objects.filter(id=pk).update(**request.data)
        return Response({"status": 1, "info": "update successful"})


# 序列化
# 导入serializer.py中自定义的序列化类
class NewCategoryView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取url上的查询字符串
        pk = kwargs.get('pk')
        if not pk:
            queryset = Category.objects.all()
            # 将查询结果序列化,many指代多行数据
            rows = New_Category_Serializer(instance=queryset, many=True, context={'request': request})
            print(rows.data)
            return Response(rows.data)
        else:
            # filter表示过滤条件
            model_object = Category.objects.filter(id=pk).first()
            ser = New_Category_Serializer(instance=model_object, many=False)
            return Response(ser.data)

    def post(self, request, *args, **kwargs):
        # 获取post传递过来的数据
        data = request.data
        print(data)
        rows = New_Category_Serializer(data=data)
        if rows.is_valid():
            rows.save()
            return Response(rows.data)
        else:
            return Response(rows.errors)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        category_object = Category.objects.filter(id=pk).first()
        ser = New_Category_Serializer(instance=category_object, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        Category.objects.filter(id=pk).delete()
        return Response('删除成功')


# 文章明细页的序列化
from .serializers import ArticleSerializer
from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle


class MySimpleRateThrottle(SimpleRateThrottle):
    scope = "limit"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


from rest_framework.permissions import IsAuthenticated


class ArticleView(APIView):
    # throttle_classes = [MySimpleRateThrottle, ]
    # 自定义分流类
    # throttle_classes = (AnonRateThrottle, UserRateThrottle,)

    # 局部认证和登录,认证和权限（必须同时存在）
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        print(request.user)
        content = {
            'user': request.user,  # `django.contrib.auth.User` instance.
            'auth': request.auth  # None
        }
        print(content)
        if not pk:
            queryset = Article.objects.all()
            ser = ArticleSerializer(instance=queryset, many=True)
            return Response(ser.data)
        article_object = Article.objects.filter(id=pk).first()
        ser = ArticleSerializer(instance=article_object, many=False)
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        ser = ArticleSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article_object = Article.objects.filter(id=pk).first()
        ser = ArticleSerializer(instance=article_object, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def patch(self, request, *args, **kwargs):
        """局部"""
        pk = kwargs.get('pk')
        article_object = Article.objects.filter(id=pk).first()
        ser = ArticleSerializer(instance=article_object, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        Article.objects.filter(id=pk).delete()
        return Response('删除成功')


# 分页查询
from .serializers import PageArticleSerializer
from rest_framework.pagination import PageNumberPagination


# 类似于Java中的接口interface，必须重写父类方法
class NewPageNumberPagination(PageNumberPagination):
    page_size = 3  # 重写，每页展示数据数


# 分页方式一
class PageViewArticleView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.all()
        """
        # 方式一：仅数据
        # 分页对象
        page_object = NewPageNumberPagination()
        # 调用 分页对象.paginate_queryset方法进行分页，得到的结果是分页之后的数据
        # result就是分完页的一部分数据
        result = page_object.paginate_queryset(queryset, request, self)
        # 序列化分页之后的数据
        ser = PageArticleSerializer(instance=result, many=True)
        return Response(ser.data)
        """

        # 方式二：数据 + 分页信息
        """
        page_object = NewPageNumberPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = PageArticleSerializer(instance=result, many=True)
        return page_object.get_paginated_response(ser.data)
        """
        # 方式三：数据 + 部分分页信息

        page_object = NewPageNumberPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = PageArticleSerializer(instance=result, many=True)
        return Response({'count': page_object.page.paginator.count, 'result': ser.data})


# 分页方式二：
from rest_framework.pagination import LimitOffsetPagination
from .serializers import PageArticleSerializer1


class HulaLimitOffsetPagination(LimitOffsetPagination):
    # 覆盖重写父类max_limit属性
    max_limit = 2


class PageArticleView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.all()
        # 声明分页类
        page_object = HulaLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = PageArticleSerializer1(instance=result, many=True)
        return Response(ser.data)


# 嘴臭生成器模块
from .serializers import NmslAndNdslSerializer


class NmslLimitOffsetPagination(LimitOffsetPagination):
    # 覆盖重写父类max_limit属性
    max_limit = 3


class Nmsl8(APIView):
    throttle_classes = [AnonRateThrottle, ]

    def get(self, request, *args, **kwargs):
        queryset = Nmsl.objects.all()
        # 声明分页类
        page_object = NmslLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = NmslAndNdslSerializer(instance=result, many=True)
        # page模式按需求自定义字段：http://api.example.org/accounts/?page=4&page_size=100
        # return Response({'count': page_object.page.paginator.count, 'result': ser.data})
        # offset模式按需要求自定义字段 http://api.example.org/accounts/?offset=400&limit=100
        return Response({'count': page_object.count, 'result': ser.data})

    def post(self, request, *args, **kwargs):
        ser = NmslAndNdslSerializer(data=request.data)
        print(request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": "success", "content": request.data.get('content')})
        else:
            return Response({"status": "failed"})

    def put(self, request, *args, **kwargs):
        """
        全部更新
        """
        pk = kwargs.get('pk')
        article_object = Nmsl.objects.filter(id=pk).first()
        ser = NmslAndNdslSerializer(instance=article_object, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def patch(self, request, *args, **kwargs):
        """局部"""
        pk = kwargs.get('pk')
        article_object = Nmsl.objects.filter(id=pk).first()
        ser = NmslAndNdslSerializer(instance=article_object, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        Nmsl.objects.filter(id=pk).delete()
        return Response('删除成功')


# 用户认证组件
from .serializers import LoginSerializer


class LoginView(APIView):
    # 注册页面
    def post(self, request, *args, **kwargs):
        user = str(request.data.get("username")).strip()
        pwd = str(request.data.get("password")).strip()
        print(user)
        print(pwd)

        user_object = UserInfo.objects.filter(username=user, password=pwd).first()
        if not user_object:
            random_string = str(uuid.uuid4())
            print(random_string)
            # 序列化
            data = {
                "username": user,
                "password": pwd,
                "token": random_string
            }
            ser = LoginSerializer(data=data)
            print(request.data)
            if ser.is_valid():
                ser.save()
                return Response({"status": "注册成功", "token": random_string})
        else:
            return Response({"status": "用户已注册"})


class MyAuthentication:
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        token = request.query_params.get('token')
        user_object = UserInfo.objects.filter(token=token).first()
        if user_object:
            return user_object, token
        return None, None


class OrderView(APIView):
    # authentication_classes = [MyAuthentication, ]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        user = request.data.get('username')
        pwd = request.data.get('password')
        print(token)
        if token and UserInfo.objects.filter(token=token):
            auth = UserInfo.objects.filter(username=user, password=pwd, token=token)
            if auth:
                return Response("order")
            else:
                return Response({"info": "用户名或密码不正确"})
        else:
            return Response({"status": "failed", "info": '登录后查看'})


class UserView(APIView):
    authentication_classes = [MyAuthentication, ]

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return Response('user')


# bilibili个人主页模块
class BIli(APIView):
    def get(self, request, *args, **kwargs):
        url = "https://api.bilibili.com/x/space/arc/search?mid=215893581&pn=1&ps=25&jsonp=jsonp"
        headers = {
            "origin": "https://space.bilibili.com",
            "referer": "https://space.bilibili.com/215893581",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
        }
        session = requests.Session()
        try:
            response = session.get(url=url, headers=headers, timeout=3)
            if response.status_code == 200:
                result = response.json()
                vlist = result["data"]["list"]["vlist"]
                page = result["data"]["page"]
                return Response({"status": 1, "vlist": vlist, "page": page})
        except Exception as e:
            return Response({"status": 0, "info": e})


# 漫画作品api
from .serializers import ComicSerializer, ComicAuthorSerializer, ComicChapterSerializer


class ComicLimitOffsetPagination(LimitOffsetPagination):
    # 覆盖重写父类max_limit属性
    max_limit = 40


class Comics(APIView):
    def get(self, request, *args, **kwargs):
        category = request.GET.get("category")
        queryset = Comic.objects.filter(category=category).order_by("-judge")
        # 声明分页类
        page_object = ComicLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = ComicSerializer(instance=result, many=True)
        # page模式按需求自定义字段：http://api.example.org/accounts/?page=4&page_size=100
        # return Response({'count': page_object.page.paginator.count, 'result': ser.data})
        # offset模式按需要求自定义字段 http://api.example.org/accounts/?offset=400&limit=100
        return Response({'count': page_object.count, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = ComicSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": "success"})
        else:
            return Response({"status": "failed"})

    # def put(self, request, *args, **kwargs):
    #     """
    #     全部更新
    #     """
    #     pk = kwargs.get('pk')
    #     article_object = Nmsl.objects.filter(id=pk).first()
    #     ser = NmslAndNdslSerializer(instance=article_object, data=request.data)
    #     if ser.is_valid():
    #         ser.save()
    #         return Response(ser.data)
    #     return Response(ser.errors)
    #
    # def patch(self, request, *args, **kwargs):
    #     """局部"""
    #     pk = kwargs.get('pk')
    #     article_object = Nmsl.objects.filter(id=pk).first()
    #     ser = NmslAndNdslSerializer(instance=article_object, data=request.data, partial=True)
    #     if ser.is_valid():
    #         ser.save()
    #         return Response(ser.data)
    #     return Response(ser.errors)
    #
    # def delete(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     Nmsl.objects.filter(id=pk).delete()
    #     return Response('删除成功')


class Comic_Author(APIView):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get("uid")
        if not uid:
            return Response({"status": "failed:请携带uid参数", "results": {}})

        queryset = Comic_author.objects.filter(uid=uid).first()
        ser = ComicAuthorSerializer(instance=queryset, many=False)
        if not ser:
            return Response({"status": "failed:请携带正确的uid参数", "results": {}})
        return Response({'status': "successful", 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = ComicAuthorSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": "success"})
        else:
            return Response({"status": "failed"})

    # def put(self, request, *args, **kwargs):
    #     """
    #     全部更新
    #     """
    #     pk = kwargs.get('pk')
    #     article_object = Nmsl.objects.filter(id=pk).first()
    #     ser = NmslAndNdslSerializer(instance=article_object, data=request.data)
    #     if ser.is_valid():
    #         ser.save()
    #         return Response(ser.data)
    #     return Response(ser.errors)
    #
    # def patch(self, request, *args, **kwargs):
    #     """局部"""
    #     pk = kwargs.get('pk')
    #     article_object = Nmsl.objects.filter(id=pk).first()
    #     ser = NmslAndNdslSerializer(instance=article_object, data=request.data, partial=True)
    #     if ser.is_valid():
    #         ser.save()
    #         return Response(ser.data)
    #     return Response(ser.errors)
    #
    # def delete(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     Nmsl.objects.filter(id=pk).delete()
    #     return Response('删除成功')


class ComicChapterLimitOffsetPagination(LimitOffsetPagination):
    # 覆盖重写父类max_limit属性
    max_limit = 800


class Comic_chapters(APIView):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get("uid")
        queryset = Comic_chapter.objects.filter(uid=uid).order_by("chapter_number")
        # 声明分页类
        page_object = ComicChapterLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = ComicChapterSerializer(instance=result, many=True)
        # page模式按需求自定义字段：http://api.example.org/accounts/?page=4&page_size=100
        # return Response({'count': page_object.page.paginator.count, 'result': ser.data})
        # offset模式按需要求自定义字段 http://api.example.org/accounts/?offset=400&limit=100
        return Response({'count': page_object.count, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = ComicChapterSerializer(data=request.data)
        # print(request.data)
        # print(ser)
        if ser.is_valid():
            ser.save()
            return Response({"status": "success"})
        else:
            return Response({"status": "failed"})


# 视频解析模块
from .middleware import bilibili_parse, haokan_parse, douyin_parse, sixroom_parse, quanmin_parse, momo_parse, \
    pearvideo_parse, meipai_parse


class VideoParse(APIView):
    throttle_classes = [AnonRateThrottle, ]

    def post(self, request, *args, **kwargs):
        category = request.data.get("category")
        if category == "1":
            uid = request.data.get("url")
            douyin = douyin_parse.DouYin(uid=uid)
            res = douyin.run()
            return Response(res)
        elif category == "3":
            bv = request.data.get("url")
            bili = bilibili_parse.Bili(bv)
            res = bili.get_url()
            return Response(res)
        elif category == "4":
            vid = request.data.get("url")
            haokan = haokan_parse.HaoKan(vid)
            res = haokan.get_url()
            return Response(res)
        elif category == "5":
            vid = request.data.get("url")
            sixRoom = sixroom_parse.sixRoom(vid)
            res = sixRoom.get_video()
            return Response(res)
        elif category == "6":
            vid = request.data.get("url")
            quanmin = quanmin_parse.QuanMin(vid)
            res = quanmin.get_info()
            return Response(res)
        elif category == "7":
            feedid = request.data.get("url")
            momo = momo_parse.MoMo(feedid)
            res = momo.get_video()
            return Response(res)
        elif category == "8":
            vid = request.data.get("url")
            pear_video = pearvideo_parse.PearVideo(vid)
            res = pear_video.get_video()
            return Response(res)
        elif category == "9":
            url = request.data.get("url")
            meiPai = meipai_parse.MeiPai(url=url)
            res = meiPai.get_video()
            return Response(res)
        else:
            return Response("兄弟萌 😘😘😘，i9正在研发中，请耐心等待佳音 🏃🏃🏃")

