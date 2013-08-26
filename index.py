#-------------------------------------------------------------------------------
#-*- coding:utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        index.py
# Purpose:
#
# Author:      daimin
#
# Created:     07-08-2013
# Copyright:   (c) daimin 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import datetime
import web
from mako.template import Template
from mako.lookup import TemplateLookup
import markdown
from web.contrib.template import render_mako
import conf
import util

#from bae.api import logging

import sys
reload(sys)
sys.setdefaultencoding('utf-8') #设置系统编码，解决BAE上面的中文编码问题

#import log

import model
import PyRSS2Gen

#logger = log.getlogger()

### Url mappings
urls = (
    r'/(\d*)', 'Index',
    r'/view/(\d*)', 'View',
    r'/tag/(\d+)/?(\d*)', 'TagHandler',
    r'/search/([^\s/]+)/?(\d*)', 'SearchHandler',
    r'/date/(\d+)/?(\d*)', 'DateHandler',
    r'/month/(\d+)/?(\d*)', 'MonthHandler',
    r'/year/(\d+)/?(\d*)', 'YearHandler',
    r'/archive/(\d{4}-\d{2})/?(\d*)', 'ArchiveHandler',
    r'/photo/?(\w*)', 'PhotoHandler',
    r'/admin/login/?', 'Login',
    r'/admin/logout/?', 'Logout',
    r'/admin/?', 'AdminHandler',
    r'/admin/menu/?', 'MenuHandler',
    r'/admin/plist/?', 'PostListHandler',
    r'/admin/new/?', 'New',
    r'/admin/delete/(\d+)', 'Delete',
    r'/admin/edit/(\d+)', 'Edit',
    r'/admin/upload/?', 'UploadHandler',
    r'/admin/del-attac/(\d+)', 'DelAttacHandler',
    r'/admin/tag-manage/?', 'TagManageHandler',
    r'/rss/(\d*)', 'RssHandler',
    #r'/static/(.*)', 'StaticHandler',
    r'/(.*)', 'StaticIndexHandler',
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates/' + conf.theme)
templates_admin_root = os.path.join(app_root, 'templates/admin')
static_root = os.path.join(app_root, 'static')

##----------------------------------------------------------
## 公共函数，web.py默认引擎使用，PhotoHandler使用的是
## web.py默认模板引擎
##----------------------------------------------------------
t_globals = {
    'datestr': web.datestr,
    'datefmt': datetime.datetime.strftime
}

##----------------------------------------------------------
## 两个render，一个前端，一个后台
##----------------------------------------------------------
render = render_mako(
        templates_root,
        input_encoding='utf-8',
        output_encoding='utf-8',
        )

render_admin = render_mako(
        templates_admin_root,
        input_encoding='utf-8',
        output_encoding='utf-8',
        )

import tempfile
#tempfile.tempdir = os.getcwd() + os.path.sep + 'temp'
#tempfile.TemporaryFile = util.TemporaryFile
#from bae.core import const
#tempfile.tempdir = const.APP_TMPDIR
 
##----------------------------------------------------------
## 公共基类
##----------------------------------------------------------
class Base():

    def __init__(self):
        self._conf = conf.site
        self.set_conf('logo_img', util.get_logo_img())
        self.login_user = util.get_login()

    def datestr(self,date):
        return web.datestr(date)

    def datefmt(self,time,fmt):
        return datetime.datetime.strftime(time, fmt)
    
    def datenow(self, fmt="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.strftime(datetime.datetime.now(), fmt)

    def get_conf(self, key):
        if self._conf.has_key(key) and self._conf[key] is not None\
           and len(self._conf[key]) > 0:
            return self._conf[key]
        else:
            return None

    def process_cont(self, cont, is_md, is_excerpt=True):
        cont = web.net.htmlunquote(cont)
        if is_excerpt:
            cont = util.excerpt(cont)
        if is_md == 1:
            cont = markdown.markdown(cont)
        return cont


    def set_conf(self, key, val):
        if self._conf is not None:
            self._conf[key] = val


    def get_recent_posts(self):
        return model.get_recent_posts()

    def get_rand_posts(self):
        return model.get_rand_posts()

    def get_tags(self):
        return model.get_tags()

    def get_archives(self):
        return model.get_archives()

    def render_page(self, currentCls):
        return util.render_page_li(self, currentCls)

    def get_sidebar(self):
        self.recentPostList = self.get_recent_posts()
        self.randPostList = self.get_rand_posts()
        self.archiveList = self.get_archives()
        self.tagCloud = self.get_tags()


##----------------------------------------------------------
## 前端处理
##----------------------------------------------------------

class Index(Base):
    def __init__(self):
        Base.__init__(self)
        self.set_conf('sub_title', None)
        self.set_conf('action_url', "/")

    def GET(self, page):
        
        tmp_posts = model.get_posts(page)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = self.process_cont(p.content, p.is_md)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)

        self.posts = newPosts
        self.pageDict = pageDict
        self.get_sidebar()

        return render.index(page=self)

class TagHandler(Base):
    def __init__(self):
        Base.__init__(self)


    def GET(self, tag, page):
        """ Show page """

        tmp_posts = model.get_posts_by_tag(tag, page)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = self.process_cont(p.content, p.is_md)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)


        self.set_conf('sub_title', tmp_posts[2].title)
        self.set_conf('action_url', '/tag/' + tag + '/')
        self.posts = newPosts
        self.pageDict = pageDict
        self.get_sidebar()

        return render.index(page=self)

class SearchHandler(Base):
    def __init__(self):
        Base.__init__(self)

    def GET(self, keyword, page):
        """ Show page """

        tmp_posts = model.get_posts(page,keyword)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = self.process_cont(p.content, p.is_md)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)

        self.set_conf('sub_title', keyword)
        self.set_conf('action_url', '/search/' + keyword + '/')
        self.posts = newPosts
        self.pageDict = pageDict
        self.get_sidebar()
        return render.index(page=self)

class DateHandler(Base):
    def __init__(self):
        Base.__init__(self)

    def GET(self, date, page):
        tmp_posts = model.get_posts_by_createtime(page, date)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = self.process_cont(p.content, p.is_md)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)

        self.set_conf('sub_title', date + u'日')
        self.set_conf('action_url', '/date/' + date + '/')
        self.posts = newPosts
        self.pageDict = pageDict
        self.get_sidebar()
        return render.index(page=self)

class MonthHandler(Base):
    def __init__(self):
        Base.__init__(self)

    def GET(self, month, page):
        tmp_posts = model.get_posts_by_createtime(page, None,month)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []

        for p in posts:
            p.content = self.process_cont(p.content, p.is_md)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)

        self.set_conf('sub_title', month + u'月')
        self.set_conf('action_url', '/month/' + month + '/')
        self.posts = newPosts
        self.pageDict = pageDict
        self.get_sidebar()
        return render.index(page=self)

class YearHandler(Base):
    def __init__(self):
        Base.__init__(self)

    def GET(self, year, page):
        tmp_posts = model.get_posts_by_createtime(page, None,None,year)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = self.process_cont(p.content, p.is_md)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)

        self.set_conf('sub_title', year + u'年')
        self.set_conf('action_url', '/year/' + year + '/')
        self.posts = newPosts
        self.pageDict = pageDict
        self.get_sidebar()
        return render.index(page=self )

class ArchiveHandler(Base):
    def __init__(self):
        Base.__init__(self)

    def GET(self, arch, page):
        tmp_posts = model.get_posts_by_createtime(page, None,None,None,arch)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = self.process_cont(p.content, p.is_md)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)

        self.set_conf('sub_title', arch)
        self.set_conf('action_url', '/archive/' + arch + '/')
        self.posts = newPosts
        self.pageDict = pageDict
        self.get_sidebar()
        return render.index(page=self )

class PhotoHandler():
    def GET(self, alb_name = ''):
        render = web.template.render(templates_root, globals=t_globals)
        photos = util.list_all_photo(conf.qiniu_bucket, 335)
        return render.photo(photos)


class RssHandler(Base):
    def __init__(self):
        Base.__init__(self)

    def GET(self, page):
        url = conf.domain
        tmp_posts = model.get_posts(page)
        posts = tmp_posts[0]
        rss_items = []

        for p in posts:
            cont = self.process_cont(p.content, p.is_md)

            #if len(cont) > 500:
            #    cont = cont[0:500] + '...'
            rssItem = PyRSS2Gen.RSSItem(
                title = p.title,
                author = conf.email,
                link = "%s/view/%d" %(url, p.id),
                description = '<![CDATA[' + cont + ']]>',
                pubDate = p.createtime
            )
            rss_items.append(rssItem)

        rss = PyRSS2Gen.RSS2(
            title = conf.site['title'],
            link = url,
            description = conf.site['description'],
            lastBuildDate = datetime.datetime.now(),
            generator = conf.site['generator'],
            language = conf.language,
            items = rss_items
            )
   
        from xml.sax import saxutils
        return saxutils.unescape(rss.to_xml("utf-8"))


class View(Base):

    def __init__(self):
        Base.__init__(self)

    def GET(self, id):
        """ View single post """
        posts = model.get_post(int(id))
        posts[0].content = self.process_cont(posts[0].content, posts[0].is_md, False)

        posts[0].tags = model.get_tag(posts[0].id)
        model.update_view_num(int(id))

        self.set_conf('sub_title', posts[0].title)
        self.post = posts[0]
        self.prevPost = posts[1]
        self.nextPost = posts[2]
        self.get_sidebar()

        return render.view(page=self)

##----------------------------------------------------------
## 后台处理
##----------------------------------------------------------
class AdminBase(Base):
    def __init__(self):
        Base.__init__(self)
        util.vali_login()
    
    def render_admin_page(self):
        return util.render_page_span(self)
    
class AdminHandler(AdminBase):
    def __init__(self):
        AdminBase.__init__(self)
        
    def GET(self):
        return render_admin.admin(page=self)
    
class MenuHandler(AdminBase):
    def __init__(self):
        AdminBase.__init__(self)
        
    def GET(self):
        return render_admin.menu(page=self)
    
class PostListHandler(AdminBase):
    def __init__(self):
        AdminBase.__init__(self)
        
    def GET(self):
        page = '1'
        keyword = ''
        x = web.input(page=None)

        if 'page' in x:
            page = x['page']
            if page is None:
                page = '1'
                
        if 'keyword' in x:
            keyword = x['keyword']
            if keyword is None:
                keyword = ''

        tmp_posts = model.get_admin_posts(page, keyword)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        self.posts = posts
        self.pageDict = pageDict
        self.action_url = web.ctx.path
        self.keyword = keyword
        return render_admin.postlist(page=self)
    
class New(AdminBase):

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
            size=30,
            description="文档标题:"),
        web.form.Textarea('content', web.form.notnull,
            rows=30, cols=80,
            description="文档内容:"),
        web.form.Textbox('tag', web.form.regexp(r".{0,200}$", '只能不多于200个字符'),
            rows=30,
            description="标签(请用,分隔):"),
        web.form.Dropdown(name='status',id="status", args=[('1', '发布'), ('0', '草稿')], 
                          value='1',description="状态"),
        web.form.File(name='attac',description="图片上传（max 512KB）"),
        web.form.Hidden(name="attacs"),
        web.form.Button('发表文档', web.form.regexp(r".*$", ''), id="submit_btn"),
    )



    def GET(self):
        form = self.form()
        return render_admin.new(page=self,form=form)

    def POST(self):
        
        form = self.form()
        if not form.validates():
            return self.render.new(page=self, form=form)
        title = web.net.htmlquote(form.d.title)

        #使用markdown不需任何操作
        #content = util.encode_newLine(form.d.content)
        #content = web.net.htmlquote(content)

        tag = web.net.htmlquote(form.d.tag)
        
        model.new_post(title, form.d.content, tag ,1, form.d.status, form.d.attacs)
        raise web.seeother('/admin/plist/')


class Delete:

    def POST(self, id):
        util.vali_login()
        model.del_post(int(id))
        raise web.seeother('/admin/plist/')
    
class DelAttacHandler:
    def POST(self, id):
        util.vali_login()
        model.del_attac_aid(int(id))
        return True

class TagManageHandler(AdminBase):
    def __init__(self):
        AdminBase.__init__(self)
        
    def GET(self):
        tags = model.get_tags_admin()
        self.tags = tags
        return render_admin.tagmanage(page=self)
    
    def POST(self):
        input_data = web.input()
        tid = input_data.tid
        action = input_data.action
        if action == "delete":
            model.del_tag_id(tid)

class Edit(AdminBase):

    def GET(self, id):
        
        posts = model.get_post(int(id))
        posts[0].content = web.net.htmlunquote(posts[0].content)
        posts[0].content = util.decode_newLine(posts[0].content)
        posts[0].tag = util.tag_implode(model.get_tag(posts[0].id))

        form = New.form()
        form.fill(posts[0])
        form.status.value = str(posts[0].status)
        ats = []
        for attac in posts[0].attacs:
            ats.append(str(attac.id))
        form.attacs.value = "|".join(ats)
        self.attacs = posts[0].attacs
    
        return render_admin.edit(page=self, form=form)


    def POST(self, id):
        util.vali_login()
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        title = web.net.htmlquote(form.d.title)
        content = util.encode_newLine(form.d.content)
        content = web.net.htmlquote(content)
        tag = web.net.htmlquote(form.d.tag)

        model.update_post(int(id), title, content, tag, form.d.status, form.d.attacs)
        raise web.seeother('/admin/plist/')

class Login():

    def GET(self):
        """ View single post """
        return render_admin.login(page=self)

    def POST(self):
        input_data = web.input()
        username = input_data.username
        password = input_data.password
        username = username.strip()
        password = password.strip()
        if username == "":
            return  render_admin.err(err='用户名不可为空')
        if password == "":
            return  render_admin.err(err='密码不可为空')

        import hashlib
        user = model.get_password_by_name(username)
        if user == None:
            return render_admin.err(err='用户不存在')
        else:
            if user.password == hashlib.md5(password).hexdigest():
                web.setcookie(conf.cookie_secure, username)
                return render_admin.success(msg='登陆成功',url="/admin/")
            else:
                return render_admin.err(err='密码错误')

class Logout():
    def GET(self):
        web.setcookie(conf.cookie_secure, None,expires="-3600")
        raise web.seeother('/')
    
class UploadHandler():
    def __init__(self):
        pass
        import cgi
        cgi.maxlen = conf.upload_max
        
    def GET(self):
        return None
    
    def POST(self):
        web.header('Content-Type', 'application/json') 
        try:
            d = web.data()
            #filedir = "c:"
            import StringIO
            s1 = StringIO.StringIO(d)
            s2 = StringIO.StringIO()
            #s.write(d)
            lines =  s1.readlines()
            file_ext = util.get_file_ext(lines[1])
            lines = lines[4:-5]
            s1.close()
               
            import time
            filename = "qiniu_%d%s" % (int(time.time() * 1000), file_ext)
            #fout = open(filedir +'/'+ filename,'wb') 
            for line in lines:
                s2.write(line)
            #fout.close()
            s2.seek(0)
            #print s2.read()
            if util.upload_pic_qiniu(s2.read(), filename):
                    #保存到数据库
                res = model.save_attac(filename)
                import json
                return json.dumps({'id':res[0],'name':filename,'url':res[1]}) 
            else:
                return False
            """
            if 'attac' in x:
                filepath = x['attac'].filename.replace('\\','/') 
                filename = filepath.split('/')[-1] 
                fileext = filepath.split('.')[-1]
                import time
                filename = "pic_%d.%s" % (int(time.time() * 1000), fileext)
                #import StringIO
                #s = StringIO.StringIO()
                #lines = x['attac'].file.readlines()
                #for line in lines:
                #    s.write(line)
                #fout = open(filedir +'/'+ filename,'wb') 
                #fout.write(x['attac'].file.read()) 
                #fout.close() # closes the file, upload complete.

                if util.upload_pic_qiniu(x['attac'].file.read(), filename):
                    #保存到数据库
                    res = model.save_attac(filename)
                    import json
                    return json.dumps({'id':res[0],'name':filename,'url':res[1]}) 
                else:
                    return False
                """
        except ValueError:
            return "File too large"

##----------------------------------------------------------
## 静态文件处理
##----------------------------------------------------------
class StaticHandler():
    def GET(self, res):
        return util.read_static(os.path.join(static_root, res))
      
class StaticIndexHandler():
    def GET(self, res):
        return util.read_static(os.path.join(app_root, res))


def errNotFound():
    render = web.template.render(templates_root, globals=t_globals)
    return web.notfound(render.e404())

########===============================================================######
web.config.debug = True
app = web.application(urls, globals())
app.notfound = errNotFound
if __name__ == "__main__":
    app.run()
#app = web.application(urls, globals()).wsgifunc()

#from bae.core.wsgi import WSGIApplication
#application = WSGIApplication(app)
