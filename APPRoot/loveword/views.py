# -*- coding:utf-8 -*-
import json
import base64
import requests
from . import models
from . import serializers
from typing import Optional, Any
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication


# 嘴臭生成器模块
class NmslLimitOffsetPagination(LimitOffsetPagination):
    # 覆盖重写父类max_limit属性
    max_limit = 3


class Nmsl8(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, *args, **kwargs):
        queryset = models.Nmsl.objects.all()
        # 声明分页类
        page_object = NmslLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = serializers.NmslAndNdslSerializer(instance=result, many=True)
        return Response({'count': page_object.count, 'result': ser.data})

    def post(self, request, *args, **kwargs):
        ser = serializers.NmslAndNdslSerializer(data=request.data)
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
        article_object = models.Nmsl.objects.filter(id=pk).first()
        ser = serializers.NmslAndNdslSerializer(instance=article_object, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def patch(self, request, *args, **kwargs):
        """局部"""
        pk: Optional[Any] = kwargs.get('pk')
        article_object = models.Nmsl.objects.filter(id=pk).first()
        ser = serializers.NmslAndNdslSerializer(instance=article_object, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        models.Nmsl.objects.filter(id=pk).delete()
        return Response('删除成功')


# bilibili个人主页模块
class BIli(APIView):
    @cache_response()
    def get(self, request, *args, **kwargs):
        queryset = models.Bilibili.objects.all().order_by("-ts")
        ser = serializers.BilibiliIndex(instance=queryset, many=True)
        return Response({"status": 1, "msg": "success", "results": ser.data})


# 漫画作品大全api模块
class ComicLimitOffsetPagination(LimitOffsetPagination):
    # 覆盖重写父类max_limit属性
    max_limit = 40


class Comics(APIView):
    def get(self, request, *args, **kwargs):
        category = request.GET.get("category")
        decode_str = base64.decodebytes(bytes(category, encoding="utf-8"))  # 字节型
        queryset = models.Comic.objects.filter(category=decode_str.decode()).order_by("-judge")
        # 声明分页类
        page_object = ComicLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = serializers.ComicSerializer(instance=result, many=True)
        return Response({'count': page_object.count, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = serializers.ComicSerializer(data=request.data)
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
        queryset = models.Comic_author.objects.filter(uid=decode_str.decode()).first()
        ser = serializers.ComicAuthorSerializer(instance=queryset, many=False)
        if not ser:
            return Response({"status": "failed:请携带正确的uid参数", "results": {}})
        return Response({'status': "successful", 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = serializers.ComicAuthorSerializer(data=request.data)
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
            queryset = models.Comic_chapter.objects.filter(uid=decode_str.decode()).order_by("chapter_number")
            # 声明分页类
            page_object = ComicChapterLimitOffsetPagination()
            result = page_object.paginate_queryset(queryset, request, self)
            ser = serializers.ComicChapterCatalogSerializer(instance=result, many=True)
            return Response({'count': page_object.count, 'results': ser.data})
        else:
            decode_str = base64.decodebytes(bytes(uid, encoding="utf-8"))
            queryset = models.Comic_chapter.objects.filter(uid=decode_str.decode(), cid=cid).first()
            ser = serializers.ComicChapterSerializer(instance=queryset, many=False)
            return Response({'status': 0, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = serializers.ComicChapterSerializer(data=request.data)
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
        # keyword定义查询条件
        keyword = request.GET.get("keyword")
        if keyword == "" or keyword is None:
            queryset = models.AVideo.objects.all().order_by("-judge")
            page_object = AVideoLimitOffsetPagination()
            result = page_object.paginate_queryset(queryset, request, self)
            ser = serializers.AVideoSerializer(instance=result, many=True)
            return Response({'count': page_object.count, 'results': ser.data})
        else:
            queryset = models.AVideo.objects.filter(title__contains=keyword).order_by("-judge")
            page_object = AVideoLimitOffsetPagination()
            result = page_object.paginate_queryset(queryset, request, self)
            ser = serializers.AVideoSerializer(instance=result, many=True)
            return Response({'count': page_object.count, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = serializers.AVideoSerializer(data=request.data)
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
        queryset = models.AVideo_chapter.objects.filter(vid=vid)
        # 声明分页类
        ser = serializers.AVideoChapterSerializer(instance=queryset, many=True)
        return Response({'status': 200, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = serializers.AVideoChapterSerializer(data=request.data)
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
        queryset = models.APicture.objects.filter(category=category)
        # 声明分页类
        page_object = AVideoLimitOffsetPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        ser = serializers.APictureSerializer(instance=result, many=True)
        return Response({'count': page_object.count, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        ser = serializers.APictureSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": "success"})
        else:
            return Response({"status": ser.errors})


# 短视频解析模块
from .middleware import bilibili_parse, haokan_parse, douyin_parse, sixroom_parse, quanmin_parse, pearvideo_parse, \
    meipai_parse, changku_parse, weibo_parse, zuiyou_parse, pipixia_parse, acfun_parse, kuaishou_parse, momo_parse, \
    kge_parse, xigua_parse, miaopai_parse, xhs_parse, xks_parse, qsp_parse, kaiyan_parse, weishi_parse, huoshan_parse, \
    huya_parse, douyin2_parse, lvzhou_parse, pipifunny, vue_parse, bixin_parse, doupai_parse, before_parse, kuxiu_parse


class VideoParse(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request, *args, **kwargs):
        res = json.loads(request.body.decode("utf-8"))
        cate = res.get("category", 1)
        signature = res.get("signature")
        timers = res.get("time")
        # base64解密category
        decode_str = base64.decodebytes(bytes(cate, encoding="utf-8"))  # 字节型
        category = decode_str.decode()
        # base64解密签名算法
        x_sign = base64.decodebytes(bytes(signature, encoding="utf-8"))
        # 获取url
        url = res.get("url")
        if x_sign.decode() != "0#badwoman%-_-%#0&" + timers:
            return Response("兄弟萌 😘😘😘，i9研发出错，请检查相关参数 ✖✖✖")
        if category == "1":
            douyin = douyin_parse.DouYin(uid=url)
            res = douyin.run()
            return Response(res)
        elif category == "3":
            bili = bilibili_parse.Bili(bv=url)
            res = bili.get_url()
            return Response(res)
        elif category == "4":
            haokan = haokan_parse.HaoKan(url=url)
            res = haokan.get_url()
            return Response(res)
        elif category == "5":
            sixRoom = sixroom_parse.sixRoom(url)
            res = sixRoom.get_video()
            return Response(res)
        elif category == "6":
            quanmin = quanmin_parse.QuanMin(url)
            res = quanmin.get_info()
            return Response(res)
        elif category == "7":
            momo = momo_parse.MoMo(url)
            res = momo.get_video()
            return Response(res)
        elif category == "8":
            pear_video = pearvideo_parse.PearVideo(url)
            res = pear_video.get_video()
            return Response(res)
        elif category == "9":
            meiPai = meipai_parse.MeiPai(url=url)
            res = meiPai.get_video()
            return Response(res)
        elif category == "10":
            changku = changku_parse.ChangKuVideo(url=url)
            res = changku.get_video()
            return Response(res)
        elif category == "11":
            weibo = weibo_parse.WeiBo(url=url)
            res = weibo.get_video()
            return Response(res)
        elif category == "12":
            zuiyou = zuiyou_parse.ZuiYou(url=url)
            res = zuiyou.get_video()
            return Response(res)
        elif category == "13":
            pipixia = pipixia_parse.PiPiXia(url=url)
            res = pipixia.get_video()
            return Response(res)
        elif category == "14":
            acfun = acfun_parse.AcFun(url=url)
            res = acfun.get_video()
            return Response(res)
        elif category == "15":
            kuaishou = kuaishou_parse.KuaiShou(url=url)
            res = kuaishou.get_video()
            return Response(res)
        elif category == "16":
            kge = kge_parse.KGe(url=url)
            res = kge.get_video()
            return Response(res)
        elif category == "17":
            xigua = xigua_parse.XiGua(url=url)
            res = xigua.get_video()
            return Response(res)
        elif category == "18":
            miaopai = miaopai_parse.MiaoPai(url=url)
            res = miaopai.get_video()
            return Response(res)
        elif category == "19":
            xhs = xhs_parse.XiaoHongShu(url=url)
            res = xhs.get_video()
            return Response(res)
        elif category == "20":
            xks = xks_parse.XiaoKaXiu(url=url)
            res = xks.get_video()
            return Response(res)
        elif category == "21":
            bbq = qsp_parse.QinShiPin(url=url)
            res = bbq.get_video()
            return Response(res)
        elif category == "22":
            open_eye = kaiyan_parse.OpenEye(url=url)
            res = open_eye.get_video()
            return Response(res)
        elif category == "23":
            wei_shi = weishi_parse.WeiShi(url=url)
            res = wei_shi.get_video()
            return Response(res)
        elif category == "24":
            huo_shan = huoshan_parse.HuoShan(url=url)
            res = huo_shan.get_video()
            return Response(res)
        elif category == "25":
            huya = huya_parse.HuYa(url=url)
            res = huya.get_video()
            return Response(res)
        elif category == "26":
            dou_yin = douyin2_parse.DouYin2(url=url)
            res = dou_yin.get_video()
            return Response(res)
        elif category == "27":
            lv_zhou = lvzhou_parse.LvZhou(url=url)
            res = lv_zhou.parse()
            return Response(res)
        elif category == "28":
            ppgx = pipifunny.PiPiFunny(url=url)
            res = ppgx.parse()
            return Response(res)
        elif category == "29":
            vue = vue_parse.Vue(url=url)
            res = vue.parse()
            return Response(res)
        elif category == "31":  # 这是使用31：因为30已经被Instagram占用了
            bi_xin = bixin_parse.BiXin(url=url)
            res = bi_xin.parse()
            return Response(res)
        elif category == "32":
            dou_pai = doupai_parse.DouPai(url=url)
            res = dou_pai.parse()
            return Response(res)
        elif category == "33":
            before = before_parse.Before(url=url)
            res = before.parse()
            return Response(res)
        elif category == "34":
            ku_xiu = kuxiu_parse.KuXiu(url=url)
            res = ku_xiu.parse()
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
        ser = serializers.CommentsSerializer(instance=result, many=True)
        return Response({'count': page_object.count, 'results': ser.data})

    # post请求创建留言板
    def post(self, request, *args, **kwargs):
        info = request.data
        cate = info.get("ip")
        decode_str = base64.decodebytes(bytes(cate, encoding="utf-8"))  # 字节型
        decode_ip = decode_str.decode()
        info["ip"] = decode_ip
        ser = serializers.CommentsSerializer(data=info)
        print(request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status": 1, "content": request.data.get('ip')})
        else:
            return Response({"status": ser.errors})


# 跨域图片下载
class FileDownload(APIView):
    def post(self, request):
        url = request.data.get("url")
        title = str(url).split("/")[-1]
        if url == "" or url is None:
            return Response({'code': 400, 'msg': '图片链接不应为空！'})
        else:
            headers = {
                "referer": "https://pixiviz.pwp.app/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36 "
            }
            try:
                result = requests.get(url=url, headers=headers, timeout=30)
                if result.status_code == 200:
                    # 获取图片的二进制
                    response = FileResponse(result.content)
                    response['Content-Type'] = 'application/octet-stream'
                    response['Content-Disposition'] = 'attachment;filename="{}"'.format(title)
                    return response
                else:
                    return Response({'code': result.status_code, 'msg': "该图片url发生未知错误"})
            except Exception as e:
                return Response({'code': -1, 'msg': str(e)})


class Quotations(APIView):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get("uid", 1)
        category = request.GET.get("category", 1)
        queryset = models.Quotation.objects.filter(id=uid, category=category)
        # 声明分页类
        ser = serializers.QuotationSerializer(instance=queryset, many=True)
        return Response({'status': 200, 'results': ser.data})

    def post(self, request, *args, **kwargs):
        res = json.loads(request.body.decode("utf-8"))
        uid = res.get("uid", 1)
        category = res.get("category", 1)
        queryset = models.Quotation.objects.filter(id=uid, category=category)
        # 声明分页类
        ser = serializers.QuotationSerializer(instance=queryset, many=True)
        return Response({'status': 200, 'results': ser.data})
