# -*- coding:utf-8 -*-
# encoding: utf-8

from bae.core import const

#数据库配置
db = {"dbn"      :"mysql",
      "dbname"   :"rccByoSlbDVOzrWdbYoA",
      "user"     :const.MYSQL_USER,
      "password" :const.MYSQL_PASS,
      "host"     : const.MYSQL_HOST,
      "port"     : int(const.MYSQL_PORT),
      }
##cookie键值
cookie_secure = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o"
##数据表前缀
tab_prefix = "to"
##是否是调试模式
DEBUG = True
##日志目录
log_dir = "log"

##文章行数，以后都是在数据库里面的
page_size = 10
##后台一页行数
page_admin_size = 20
##主题
theme = "white_p"

##域名
domain = "http://codecos.com"
##站长email
email = "daiming253685@126.com"

##语言
language = 'zh-cn'
##列表大小
list_size = 20
##摘抄的大小
excerpt_size = 500
##上传文件大小(512kb)
upload_max = 512 * 1024  

##网站配置
site = {
    "keywords":u"记忆,过去,生活,工作,技术,java,python,php,nodejs,golang,linux",
    "description":u"记录生活的点点滴滴，记录工作学习的感悟",
    "title":u"codecos",
    ##生成工具
    "generator" : "tologd",
        }
##七牛存储配置
qiniu_access_key = "uhmPwUv-z5Lddn0B6spCfeFVmh25VXCvmXmqMDz3"
qiniu_secret_key = "0H5WGOO_wP-R7kup11If3hFq-1vYNUPFXeohFmzN"
#vagasnail空间
qiniu_domain = "vagasnail.qiniudn.com"
qiniu_bucket = "vagasnail"
#vaga-static空间
qiniu_bucket2 = "vaga-static"
qiniu_domain2 = "vaga-static.qiniudn.com"
