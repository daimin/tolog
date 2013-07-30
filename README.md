# tolog是一款部署在BAE上面的基于web.py的博客程序
**部署该博客需要：**

1.  申请[BAE](http://developer.baidu.com/dev#/create)
2.  [web.py](http://webpy.org)不需要下载，BAE默认有web.py环境
3.  配置BAE的URL，具体见app.conf，其实你需要SVN下来你的BAE项目，然后将app.conf中的配置拷贝进去就行了
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
