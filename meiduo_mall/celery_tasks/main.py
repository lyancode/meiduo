from celery import Celery


celery_app = Celery('meiduo')

# 导入配置文件
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])


# 开启celery的命令
#  celery -A 应用路径（.包路径） worker -l info
#  celery -A celery_tasks.main worker -l info