# -*- coding:utf-8 -*-
# encoding: utf-8

#from bae.core import const

#数据库配置
db = {"dbn"      :"mysql",
      #"dbname"   :"rccByoSlbDVOzrWdbYoA",
      #"user"     :const.MYSQL_USER,
      #"password" :const.MYSQL_PASS,
      #"host"     : const.MYSQL_HOST,
      #"port"     : int(const.MYSQL_PORT),
      "dbname"   :"webpy_blog",
      "user"     :"root",
      "password" :"daimin",
      "host"     : "localhost",
      "port"     : 3306,
      }

cookie_secure = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o"

tab_prefix = "to"

AutoReload = True
DEBUG = True
#视图控制模块名
view_controller_modules = ""

log_dir = "log"

#文章行数，以后都是在数据库里面的
page_size = 15
