from django.db import models
from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData
import time
from django.template import Context, Template
from wechat import send_msg
from os import environ as env
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


wechat_template = """ {{ service.name }}  {% if service.overall_status != service.PASSING_STATUS %} 异常, 状态： {{ service.overall_status }}{% else %} 已回归正常 {% endif %}.
{% if service.overall_status != service.PASSING_STATUS %}
Failing checks:{% for check in service.all_failing_checks %}
  FAILING - {{ check.name }} - ({{ check.last_result.error | safe }}) {% endfor %}
{% if service.all_passing_checks %}
Passing checks:{% for check in service.all_passing_checks %}
  PASSING - {{ check.name }} - {% endfor %}
{% endif %}
{% endif %}
"""

class WechatAlert(AlertPlugin):
    name = "Wechat Alert"
    author = "xiaolong.yuanxl"

    def send_alert(self, service, users, duty_officers):
        """Implement your send_alert functionality here."""

        # 从 conf 配置文件获取 环境变量
        corpid = env.get('WECHAT_CORP_ID')
        corpsecret = env.get('WECHAT_CORP_SECRET')
        appid = env.get('WECHAT_APPID')
        partyid = env.get('WECHAT_PARTY_ID')


        # 获取 service 状态 如果不是 PASSING 则报警
        if service.overall_status != service.PASSING_STATUS:
            title = ' %s 状态 %s' % (service.name, service.overall_status)
        else:
            title = '%s back to normal ' % (service.name,)


        # 渲染正文
        t = Template(wechat_template)
        c = Context({
            'service': service
        })
        content = t.render(c)

        # 记日志
        print "[Wechat Alert] 时间:{0}\n标题:{1}\n内容:{2}".format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),title, content)

        # 发送逻辑
        send_msg(title,content,corpid,corpsecret,appid,partyid)

        return

class WechatAlertUserData(AlertPluginUserData):
    name = "Wechat Plugin"
    favorite_bone = models.CharField(max_length=50, blank=True)

