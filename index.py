#-*- coding:utf-8 -*-

""" Basic blog using webpy 0.3 """
import os
import datetime
import web
import markdown

import conf
import util

#import log

import model
import PyRSS2Gen

#logger = log.getlogger()

### Url mappings 

urls = (
    r'/(\d*)', 'Index',
    r'/view/(\d*)', 'View',
    r'/new', 'New',
    r'/delete/(\d+)', 'Delete',
    r'/edit/(\d+)', 'Edit',
    r'/tag/(\d+)/?(\d*)', 'TagHandler',
    r'/search/([^\s/]+)/?(\d*)', 'SearchHandler',
    r'/date/(\d+)/?(\d*)', 'DateHandler',
    r'/month/(\d+)/?(\d*)', 'MonthHandler',
    r'/year/(\d+)/?(\d*)', 'YearHandler',
    r'/login/?', 'Login',
    r'/logout/?', 'Logout',
    r'/rss/(\d*)', 'RssHandler',
    r'/static/(.*)', 'StaticHandler',
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
static_root = os.path.join(app_root, 'static')

### Templates
t_globals = {
    'datestr': web.datestr,
    'datefmt': datetime.datetime.strftime
}

render = web.template.render(templates_root, base='base', globals=t_globals)


class Index:

    def GET(self, page):
        """ Show page """
        
        tmp_posts = model.get_posts(page)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = web.net.htmlunquote(p.content)
            if p.is_md == 1:
                p.content = markdown.markdown(p.content)
            
            p.tags = model.get_tag(p.id)
            newPosts.append(p)
        
        return render.index(newPosts, pageDict, util.get_login(), '/')

class TagHandler():
    def GET(self, tag, page):
        """ Show page """
        
        tmp_posts = model.get_posts_by_tag(tag, page)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = web.net.htmlunquote(p.content)
            if p.is_md == 1:
                p.content = markdown.markdown(p.content)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)
        
        return render.index(newPosts, pageDict, util.get_login(), '/tag/' + tag + '/')

class SearchHandler():
    def GET(self, keyword, page):
        """ Show page """
        
        tmp_posts = model.get_posts(page,keyword)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = web.net.htmlunquote(p.content)
            if p.is_md == 1:
                p.content = markdown.markdown(p.content)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)
        
        return render.index(newPosts, pageDict, util.get_login(), '/search/' + keyword + '/' )
    
class DateHandler():
    def GET(self, date, page):
        tmp_posts = model.get_posts_by_createtime(page, date)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = web.net.htmlunquote(p.content)
            if p.is_md == 1:
                p.content = markdown.markdown(p.content)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)
        
        return render.index(newPosts, pageDict, util.get_login(), '/date/' + date + '/' )
    
class MonthHandler():
    def GET(self, month, page):
        tmp_posts = model.get_posts_by_createtime(page, None,month)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = web.net.htmlunquote(p.content)
            if p.is_md == 1:
                p.content = markdown.markdown(p.content)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)
        
        return render.index(newPosts, pageDict, util.get_login(), '/month/' + month + '/' )
    
class YearHandler():
    def GET(self, year, page):
        tmp_posts = model.get_posts_by_createtime(page, None,None,year)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = web.net.htmlunquote(p.content)
            if p.is_md == 1:
                p.content = markdown.markdown(p.content)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)
        
        return render.index(newPosts, pageDict, util.get_login(), '/year/' + year + '/' )
    
class RssHandler():
    def GET(self, page):
        url = 'http://tologd.duapp.com'
        tmp_posts = model.get_posts(page)
        posts = tmp_posts[0]
        rss_items = []
        
        for p in posts:
            p.content = web.net.htmlunquote(p.content)
            if p.is_md == 1:
                p.content = markdown.markdown(p.content)
            cont = p.content
            
            #if len(cont) > 500:
            #    cont = cont[0:500] + '...'
            rssItem = PyRSS2Gen.RSSItem(
                title = p.title,
                author = "daimin253685#126.com",
                link = "%s/view/%d" %(url, p.id),
                description = '<![CDATA[' + cont + ']]>',
                pubDate = p.createtime
            )
            print rssItem.description
            rss_items.append(rssItem)
        
        rss = PyRSS2Gen.RSS2(
            title = u"点滴记忆",
            link = url,
            description = u"点滴记忆,致我们的过去与未来",
            lastBuildDate = datetime.datetime.now(),
            generator = "tologd",
            language = 'zh-cn',
            items = rss_items
            )
        from xml.sax import saxutils
        return saxutils.unescape(rss.to_xml("utf-8"))

class View:

    def GET(self, id):
        """ View single post """
        posts = model.get_post(int(id))
        posts[0].content = web.net.htmlunquote(posts[0].content)
        if posts[0].is_md == 1:            
            posts[0].content = markdown.markdown(posts[0].content)
            
        posts[0].tags = model.get_tag(posts[0].id)
        model.update_view_num(int(id)) 
        return render.view(posts[0],posts[1],posts[2], util.get_login())


class New:

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
        web.form.Button('发表文档', web.form.regexp(r".*$", ''), id="submit_btn"),
    )

    def __init__(self):
        self.render = web.template.render(templates_root,base='admin_base', globals=t_globals)
        
    
    def GET(self):
        util.vali_login()
        form = self.form()
        return self.render.new(form)

    def POST(self):
        util.vali_login()
        form = self.form()
        if not form.validates():
            return self.render.new(form)
        title = web.net.htmlquote(form.d.title)
        
        #使用markdown不需任何操作
        #content = util.encode_newLine(form.d.content)
        #content = web.net.htmlquote(content)
        
        tag = web.net.htmlquote(form.d.tag)
        model.new_post(title, form.d.content, tag ,1)
        raise web.seeother('/')


class Delete:

    def POST(self, id):
        util.vali_login()
        model.del_post(int(id))
        raise web.seeother('/')


class Edit:

    def GET(self, id):
        util.vali_login()
        render = web.template.render(templates_root,base='admin_base', globals=t_globals)
        posts = model.get_post(int(id))
        posts[0].content = web.net.htmlunquote(posts[0].content)
        posts[0].content = util.decode_newLine(posts[0].content)
        posts[0].tag = util.tag_implode(model.get_tag(posts[0].id))
        
        form = New.form()
        form.fill(posts[0])
        return render.edit(posts[0], form)


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
        
        model.update_post(int(id), title, content, tag)
        raise web.seeother('/')
    
class Login():
    
    def GET(self):
        """ View single post """
        render = web.template.render('templates', globals=t_globals)
        return render.login()
    
    def POST(self):
        input_data = web.input()
        render = web.template.render('templates', globals=t_globals)
        username = input_data.username
        password = input_data.password
        username = username.strip()
        password = password.strip()
        if username == "":
            return  render.err(err='用户名不可为空')
        if password == "":
            return  render.err(err='密码不可为空')
        
        import hashlib
        user = model.get_password_by_name(username)
        if user == None:
            return render.err(err='用户不存在')
        else:
            if user.password == hashlib.md5(password).hexdigest():
                web.setcookie(conf.cookie_secure, username) 
                return render.success(msg='登陆成功',url="/")
            else:
                return render.err(err='密码错误')
            
class Logout():
    def GET(self):
        web.setcookie(conf.cookie_secure, None,expires="-3600") 
        raise web.seeother('/')
            
class StaticHandler():
    def GET(self, res):
        return util.read_static(os.path.join(static_root, res))
            
    

########===============================================================######
web.config.debug = True
app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
#app = web.application(urls, globals()).wsgifunc()
 
#from bae.core.wsgi import WSGIApplication
#application = WSGIApplication(app)
