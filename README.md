### tolog是一款部署在BAE上面的基于web.py的博客程序
这个是一个非常简单的博客程序，只实现了文章列表，文档浏览，登陆，编辑/添加文章等几个有限的功能。

**部署该博客需要:**

+  申请[BAE](http://developer.baidu.com/dev#/create)
+  [web.py](http://webpy.org)不需要下载，BAE默认有web.py环境
+  配置BAE的URL，具体见`app.conf`，其实你需要SVN下来你的BAE项目，然后将`app.conf`中的配置拷贝进去就行了

**BAE配置URL:**

    \- url : /(\d*)
      script : index.py
    \- url : /new
      script : index.py
    \- url : /view/(\d*)
      script : index.py
    \- url : /delete/(\d+)
      script : index.py
    \- url : /login/?
      script : index.py
    \- url : /edit/(\d+)
      script : index.py
    \- url : /tag/(\d+)/?(\d*)
      script : index.py
    \- url : /search/([^\s/]+)/?(\d*)
      script : index.py
    \- url : /date/(\d+)/?(\d*)
      script : index.py
    \- url : /month/(\d+)/?(\d*)
      script : index.py
    \- url : /year/(\d+)/?(\d*)
      script : index.py
    \- url : logout/?
      script : index.py
    \- url : /rss/(\d*)
      script : index.py
    \- url : /static/(.*)
      script : index.py
      
+ 修改`conf.py`中的数据库配置为BAE所要求的格式

**数据库配置**

    db = {"dbn"      :"mysql",
          "dbname"   :"rccByoSlbDVOzrWdbYoA",
          "user"     :const.MYSQL_USER,
          "password" :const.MYSQL_PASS,
          "host"     : const.MYSQL_HOST,
          "port"     : int(const.MYSQL_PORT),
    }

+ 修改`index.py`中的运行环境由本机为BAE运行环境

**BAE的web.py运行环境**

    app = web.application(urls, globals()).wsgifunc()
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(app)
    
    

