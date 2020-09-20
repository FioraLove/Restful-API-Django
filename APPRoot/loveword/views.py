from typing import Optional, Any
import requests
import base64
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Nmsl, Comic, Comic_chapter, Comic_author, AVideo, AVideo_chapter, APicture
from .serializers import NmslAndNdslSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination  # 分页方式二
from .serializers import ComicSerializer, ComicAuthorSerializer, ComicChapterSerializer, AVideoSerializer, \
    AVideoChapterSerializer, APictureSerializer


# 嘴臭生成器模块
class NmslLimitOffsetPagination(LimitOffsetPagination):
    # 覆盖重写父类max_limit属性
    max_limit = 3


class Nmsl8(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, *args, **kwargs):
        queryset = Nmsl.objects.all()
        # 声明分页类
        page_object = NmslLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = NmslAndNdslSerializer(instance=result, many=True)
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
        pk: Optional[Any] = kwargs.get('pk')
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


# # bilibili个人主页模块
# class BiLiStar(APIView):
#     def get(self, request, *args, **kwargs):
#         pass


# 漫画作品大全api模块
class ComicLimitOffsetPagination(LimitOffsetPagination):
    # 覆盖重写父类max_limit属性
    max_limit = 40


class Comics(APIView):
    def get(self, request, *args, **kwargs):
        category = request.GET.get("category")
        decode_str = base64.decodebytes(bytes(category, encoding="utf-8"))  # 字节型
        queryset = Comic.objects.filter(category=decode_str.decode()).order_by("-judge")
        # 声明分页类
        page_object = ComicLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = ComicSerializer(instance=result, many=True)
        return Response({'count': page_object.count, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = ComicSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": "success"})
        else:
            return Response({"status": ser.errors})


# 漫画作者相关信息模块
class Comic_Author(APIView):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get("uid")
        if not uid:
            return Response({"status": "failed:请携带uid参数", "results": {}})
        decode_str = base64.decodebytes(bytes(uid, encoding="utf-8"))
        queryset = Comic_author.objects.filter(uid=decode_str.decode()).first()
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


# 漫画章节分页模块
class ComicChapterLimitOffsetPagination(LimitOffsetPagination):
    # 覆盖重写父类max_limit属性
    max_limit = 800


class Comic_chapters(APIView):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get("uid")
        decode_str = base64.decodebytes(bytes(uid, encoding="utf-8"))
        queryset = Comic_chapter.objects.filter(uid=decode_str.decode()).order_by("chapter_number")
        # 声明分页类
        page_object = ComicChapterLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = ComicChapterSerializer(instance=result, many=True)
        return Response({'count': page_object.count, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = ComicChapterSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": "success"})
        else:
            return Response({"status": ser.errors})


# 隐私加密视频主页
class AVideoLimitOffsetPagination(LimitOffsetPagination):
    # 覆盖重写父类max_limit属性
    max_limit = 50


class AVideos(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        queryset = AVideo.objects.all().order_by("-judge")
        # 声明分页类
        page_object = AVideoLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = AVideoSerializer(instance=result, many=True)
        return Response({'count': page_object.count, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = AVideoSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": "success"})
        else:
            return Response({"status": ser.errors})


# 隐私加密视频的集数以及其播放地址
class AVideoChapters(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        vid = request.GET.get("vid")
        queryset = AVideo_chapter.objects.filter(vid=vid)
        # 声明分页类
        ser = AVideoChapterSerializer(instance=queryset, many=True)
        return Response({'status': 200, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = AVideoChapterSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": "success"})
        else:
            return Response({"status": ser.errors})


# 隐私加密图片大全
class AImages(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        category = request.GET.get("category")
        queryset = APicture.objects.filter(category=category)
        # 声明分页类
        page_object = AVideoLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = APictureSerializer(instance=result, many=True)
        return Response({'count': page_object.count, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = APictureSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": "success"})
        else:
            return Response({"status": ser.errors})


# 短视频解析模块
from .middleware import bilibili_parse, haokan_parse, douyin_parse, sixroom_parse, quanmin_parse, momo_parse, \
    pearvideo_parse, meipai_parse, changku_parse, weibo_parse


class VideoParse(APIView):
    throttle_classes = [AnonRateThrottle, ]

    def post(self, request, *args, **kwargs):
        cate = request.data.get("category")
        decode_str = base64.decodebytes(bytes(cate, encoding="utf-8"))  # 字节型
        category = decode_str.decode()
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
        elif category == "10":
            url = request.data.get("url")
            changku = changku_parse.ChangKuVideo(url=url)
            res = changku.get_video()
            return Response(res)
        elif category == "11":
            url = request.data.get("url")
            weibo = weibo_parse.WeiBo(url=url)
            res = weibo.get_video()
            return Response(res)
        else:
            return Response("兄弟萌 😘😘😘，i9正在研发中，请耐心等待佳音 🏃🏃🏃")
