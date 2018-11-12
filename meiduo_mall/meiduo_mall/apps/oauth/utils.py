from django.conf import settings
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
import logging
import json

from .exceptions import QQAPIException

logger = logging.getLogger('django')


class OAuthQQ(object):
    """
    用户QQ登录的工具类
    提供了QQ登录可能使用的方法
    """

    def __init__(self, app_id=None, app_key=None, redirect_uri=None, state=None):
        self.app_id = app_id or settings.QQ_APP_ID
        self.app_key = app_key or settings.QQ_APP_KEY
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URL
        self.state = state or settings.QQ_STATE

    def generate_qq_login_url(self):
        """
        拼接用户QQ登录的链接地址
        :return: 链接地址
        """
        url = 'https://graph.qq.com/oauth2.0/authorize?'
        data = {
            'response_type': 'code',
            'client_id': self.app_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
            'scope': 'get_user_info'  # 获取用户的qq的openid
        }

        query_string = urlencode(data)
        url += query_string
        # print(url)

        return url

    def get_access_token(self, code):
        """
        获取qq的acess_token
        :param code: 调用的凭据
        :return: access_token
        """
        url = 'https://graph.qq.com/oauth2.0/token?'
        req_data = {
            'grant_type': 'authorization_code',
            'client_id': self.app_id,
            'client_secret': self.app_key,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        url += urlencode(req_data)

        try:
            # 发送请求
            response = urlopen(url)
            # 读取qq返回的响应提数据
            response = response.read().decode()
            # 将返回的数据转换为字典
            resp_dict = parse_qs(response)

            access_token = resp_dict.get("access_token")[0]
        except Exception as e:
            logger.error(e)
            raise QQAPIException('获取access_token异常')

        return access_token

    def get_openid(self, access_token):
        """
        获取用户openid
        :param access_token: qq提供的access token
        :return: open_id
        """
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token
        try:
            response = urlopen(url)
            response_data = response.read().decode()
            # 返回的数据 callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} )\n;
            data = json.loads(response_data[10:-4])
        except Exception:
            data = parse_qs(response_data)
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise QQAPIException('获取openid异常')

        openid = data.get('openid', None)
        return openid
