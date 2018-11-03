import random

from django.http.response import HttpResponse
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from meiduo_mall.libs.captcha.captcha import captcha

from meiduo_mall.libs.yuntongxun.sms import CCP
from . import constants
from . import serializers


class ImageCodeView(APIView):
    """
    图片验证码
    """

    def get(self, request, image_code_id):
        """获取图片验证码"""
        # 生成图片验证码
        text, image = captcha.generate_captcha()
        # 获取redis的连接对象
        redis_conn = get_redis_connection("verify_codes")
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        return HttpResponse(image, content_type="images/jpg")


class SMSCodeView(GenericAPIView):
    """短信验证码"""
    serializer_class = serializers.ImageCodeCheckSerializers

    def get(self, request, mobile):
        # 校验图片验证码和发送短信的频次
        # mobile是被放到了类视图属性kwargs中
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 校验通过、生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)

        # 保存验证码以及发送记录
        redis_conn = get_redis_connection('verify_codes')
        # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 使用redis的pipeline管道一次执行多条redis命令
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()

        # 发送短信
        ccp = CCP()
        time = str(constants.SMS_CODE_REDIS_EXPIRES / 60)
        ccp.send_template_sms(mobile, [sms_code, time], constants.SMS_CODE_TEMP_ID)

        return Response({'message': 'OK'})
