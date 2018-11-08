from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import OAuthQQ

# Create your views here.


class OAuthQQURLView(APIView):
    """
    提供QQ登录的网址
    前端请求接口网址 /oauth/qq/authorization/?state=xxxxxx
    state参数是由前端传递,参数值为在qq成功登录后,我们后端把用户引导到那个美多商城页面
    """

    def get(self, request):
        # 提取state参数
        state = request.query_params.get('state')
        if not state:
            state = '/'  # 若前端未指明则跳转至首页

        # 按照QQ的说明文档,拼接用户QQ登录的链接地址
        oauth_qq = OAuthQQ(state=state)
        login_url = oauth_qq.generate_qq_login_url()

        # 返回链接地址
        return Response({"oauth_url": login_url})
