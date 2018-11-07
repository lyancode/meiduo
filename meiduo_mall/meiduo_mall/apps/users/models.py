from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData
from django.conf import settings

from . import constants


# Create your models here.
class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_send_sms_code_token(self):
        """
        生成发送短信验证码的access_token
        :return: access_token
        """
        # 创建itsdangerous模型的转换工具
        serializer = TJWSSerializer(settings.SECRET_KEY, constants.SEND_SMS_CODE_TOKEN_EXIPIRES)
        data = {
            'mobile': self.mobile
        }
        token = serializer.dumps(data)

        return token.decode()


    @staticmethod
    def check_send_sms_code_token(token):
        """
        校验access token
        :param token: access tokern
        :return: mobile None
        """
        serialier = TJWSSerializer(settings.SECRET_KEY, constants.SEND_SMS_CODE_TOKEN_EXIPIRES)
        try:
            data = serialier.loads(token)
        except BadData:
            return None
        else:
            mobile = data.get('mobile')
            return mobile
