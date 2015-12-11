Cabot Wechat Plugin
=====

## 简介

利用「微信企业号」进行报警 ，微信企业号的注册过程，请参考这篇文章 [zabbix如何实现微信报警](http://wuhf2015.blog.51cto.com/8213008/1688614)

微信发送原理：
Step1. 根据微信企业号属性 CorpId 和 Secret 向服务接口，获取本次请求 Token
Step2. 携带刚才返回的 Token ，向消息接口发送 post 请求

效果：![1](https://github.com/yuanxiaolong/cabot-alert-wechat/raw/master/img/wechat_alert.png)


---

## 插件安装

前置：
* 已进入cabot的安装目录，例如 ``` /usr/local/datacenter/cabot ```
* 已停止 cabot 相关进程，有2组进程。
    * 消息队列处理进程 ```ps -ef | grep python | grep celery``` 10个进程
    * UI 进程 ``` ps -ef | grep python | grep manage.py ``` 1个进程（或许你有其他 django 应用在运行，请自己通过端口区分）
  如果你实在记不清，也可以通过启动日志查看，类似这样的日志
  ```
  14:04:00 web.1    | started with pid 36652
  14:04:00 celery.1 | started with pid 36653
  ```
* 已注册了一个 「微信企业号」，并有 「CorpID」和「Secret」及「应用ID」和「接收组ID」。如果记不住 「CorpID」和「Secret」可以在 微信公共号后台
  「设置」-> 「权限管理」->「你自己建的组名」 最下面有
* 已通过 [微信企业号接口调试工具](http://qydev.weixin.qq.com/debug) 调试OK了微信账号，附上[发送接口说明](http://qydev.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F)


1.编写配置文件,添加 插件名称（注意是下划线，不是工程名，而是里面的 模块名，由setup.py里指定的）, 并修改 ```setup.py``` 内的相关信息

```
vi conf/development.env

# Plugins to be loaded at launch
CABOT_PLUGINS_ENABLED=cabot_alert_hipchat==1.7.0,cabot_alert_twilio==1.6.1,cabot_alert_email==1.3.1,cabot_alert_wechat==0.0.1

```

2.通过 pip 安装自定义插件

```
pip install git+git://github.com/yuanxiaolong/cabot-alert-wechat.git
```

3.初始化数据库

```
sh setup_dev.sh
```

4.无误后，启动 cabot

``` nohup foreman start & ```

---

## 插件编写

官方更详细的 文档 [http://cabotapp.com/dev/writing-alert-plugins.html](http://cabotapp.com/dev/writing-alert-plugins.html)