from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.views import APIView

from meiduo_mall.libs.captcha.captcha import captcha
from . import constants


class ImageCodeView(APIView):
    """
    图片验证码
    """
    def get(self, request, image_code_id):
        """获取图片验证码"""
        # 生成图片验证码
        text, image = captcha.generate_captcha()
        # 获取redis的连接对象
        redis_conn  =get_redis_connection("verify_codes")
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        return HttpResponse(image, content_type="images/jpg")