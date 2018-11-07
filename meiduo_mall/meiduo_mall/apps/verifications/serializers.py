from django_redis import get_redis_connection
from redis.exceptions import RedisError
from rest_framework import serializers
import logging

logger = logging.getLogger('django')


class ImageCodeCheckSerializers(serializers.Serializer):
    """
    图片验证码校验序列化器
    """
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(min_length=4, max_length=4)

    def validate(self, attrs):
        """
        校验
        """
        image_code_id = attrs['image_code_id']
        text = attrs['text']

        # 查询真实的图片验证码
        redis_conn = get_redis_connection('verify_codes')
        real_image_code_text = redis_conn.get('img_%s' % image_code_id)

        if not real_image_code_text:
            # 过期或不存在
            raise serializers.ValidationError("图片验证码无效")

        # 删除redis中的图片验证，防止用户对同意验证码进行重复验证
        try:
            redis_conn.delete('img_%s' % image_code_id)
        except RedisError as e:
            logger.error(e)

        # 比较图片验证码
        real_image_code_text = real_image_code_text.decode()
        if real_image_code_text.lower() != text.lower():
            raise serializers.ValidationError("图片验证码错误")

        # 判断是否在60秒内
        mobile = self.context['view'].kwargs.get('mobile')
        if mobile:
            send_flag = redis_conn.get('send_flag_%s' % mobile)
            if send_flag:
                raise serializers.ValidationError("发送短信过于频繁")

        return attrs
