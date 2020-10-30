from typing import Optional, Any
import requests
import base64
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Nmsl, Comic, Comic_chapter, Comic_author, AVideo, AVideo_chapter, APicture
from . import models
from .serializers import NmslAndNdslSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework.pagination import LimitOffsetPagination  # 分页方式二
from .serializers import ComicSerializer, ComicAuthorSerializer, ComicChapterSerializer, AVideoSerializer, \
    AVideoChapterSerializer, APictureSerializer, CommentsSerializer, ComicChapterCatalogSerializer


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
    @cache_response()
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
    max_limit = 40


class Comic_chapters(APIView):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get("uid")
        cid = request.GET.get("cid")
        if not cid:
            decode_str = base64.decodebytes(bytes(uid, encoding="utf-8"))
            queryset = Comic_chapter.objects.filter(uid=decode_str.decode()).order_by("chapter_number")
            # 声明分页类
            page_object = ComicChapterLimitOffsetPagination()
            result = page_object.paginate_queryset(queryset, request, self)
            ser = ComicChapterCatalogSerializer(instance=result, many=True)
            return Response({'count': page_object.count, 'results': ser.data})
        else:
            decode_str = base64.decodebytes(bytes(uid, encoding="utf-8"))
            queryset = Comic_chapter.objects.filter(uid=decode_str.decode(), cid=cid).first()
            ser = ComicChapterSerializer(instance=queryset, many=False)
            return Response({'status': 0, 'results': ser.data})

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
from .middleware import bilibili_parse, haokan_parse, douyin_parse, sixroom_parse, quanmin_parse, pearvideo_parse, \
    meipai_parse, changku_parse, weibo_parse, zuiyou_parse, pipixia_parse, acfun_parse, kuaishou_parse, momo_parse, \
    kge_parse, xigua_parse, miaopai_parse, xhs_parse, xks_parse, qsp_parse, kaiyan_parse, weishi_parse, huoshan_parse,\
    huya_parse, douyin2_parse, lvzhou_parse


class VideoParse(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request, *args, **kwargs):
        cate = request.data.get("category")
        signature = request.data.get("signature")
        timers = request.data.get("time")
        # base64解密category
        decode_str = base64.decodebytes(bytes(cate, encoding="utf-8"))  # 字节型
        category = decode_str.decode()
        # base64解密签名算法
        x_sign = base64.decodebytes(bytes(signature, encoding="utf-8"))
        if x_sign.decode() != "0#badwoman%-_-%#0&" + timers:
            return Response("兄弟萌 😘😘😘，i9研发出错，请检查相关参数 ✖✖✖")
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
        elif category == "12":
            url = request.data.get("url")
            zuiyou = zuiyou_parse.ZuiYou(url=url)
            res = zuiyou.get_video()
            return Response(res)
        elif category == "13":
            url = request.data.get("url")
            pipixia = pipixia_parse.PiPiXia(url=url)
            res = pipixia.get_video()
            return Response(res)
        elif category == "14":
            url = request.data.get("url")
            acfun = acfun_parse.AcFun(url=url)
            res = acfun.get_video()
            return Response(res)
        elif category == "15":
            url = request.data.get("url")
            kuaishou = kuaishou_parse.KuaiShou(url=url)
            res = kuaishou.get_video()
            return Response(res)
        elif category == "16":
            url = request.data.get("url")
            kge = kge_parse.KGe(url=url)
            res = kge.get_video()
            return Response(res)
        elif category == "17":
            url = request.data.get("url")
            xigua = xigua_parse.XiGua(url=url)
            res = xigua.get_video()
            return Response(res)
        elif category == "18":
            url = request.data.get("url")
            miaopai = miaopai_parse.MiaoPai(url=url)
            res = miaopai.get_video()
            return Response(res)
        elif category == "19":
            url = request.data.get("url")
            xhs = xhs_parse.XiaoHongShu(url=url)
            res = xhs.get_video()
            return Response(res)
        elif category == "20":
            url = request.data.get("url")
            xks = xks_parse.XiaoKaXiu(url=url)
            res = xks.get_video()
            return Response(res)
        elif category == "21":
            url = request.data.get("url")
            bbq = qsp_parse.QinShiPin(url=url)
            res = bbq.get_video()
            return Response(res)
        elif category == "22":
            url = request.data.get("url")
            open_eye = kaiyan_parse.OpenEye(url=url)
            res = open_eye.get_video()
            return Response(res)
        elif category == "23":
            url = request.data.get("url")
            wei_shi = weishi_parse.WeiShi(url=url)
            res = wei_shi.get_video()
            return Response(res)
        elif category == "24":
            url = request.data.get("url")
            huo_shan = huoshan_parse.HuoShan(url=url)
            res = huo_shan.get_video()
            return Response(res)
        elif category == "25":
            url = request.data.get("url")
            huya = huya_parse.HuYa(url=url)
            res = huya.get_video()
            return Response(res)
        elif category == "26":
            url = request.data.get("url")
            dou_yin = douyin2_parse.DouYin2(url=url)
            res = dou_yin.get_video()
            return Response(res)
        elif category == "27":
            url = request.data.get("url")
            lv_zhou = lvzhou_parse.LvZhou(url=url)
            res = lv_zhou.parse()
            return Response(res)
        else:
            return Response("兄弟萌 😘😘😘，i9正在研发中，请耐心等待佳音 🏃🏃🏃")


# 留言，回复模块
class Comments_Reply(APIView):
    # get请求分页查询
    def get(self, request, *args, **kwargs):
        queryset = models.Comments.objects.all().values("ip", "uid", "contents", "reply", "update",
                                                        "location").order_by("-update")
        # 声明分页类(借用之前隐私视频的分页功能)
        page_object = AVideoLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = CommentsSerializer(instance=result, many=True)
        return Response({'count': page_object.count, 'results': ser.data})

    # post请求创建留言板
    def post(self, request, *args, **kwargs):
        info = request.data
        cate = info.get("ip")
        decode_str = base64.decodebytes(bytes(cate, encoding="utf-8"))  # 字节型
        decode_ip = decode_str.decode()
        info["ip"] = decode_ip
        ser = CommentsSerializer(data=info)
        print(request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": 1, "content": request.data.get('ip')})
        else:
            return Response({"status": ser.errors})
