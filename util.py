# -*- coding:utf-8 -*-
# encoding: utf-8
import conf
import math
import sys
import web

import qiniu.conf
qiniu.conf.ACCESS_KEY = conf.qiniu_access_key
qiniu.conf.SECRET_KEY = conf.qiniu_secret_key


import qiniu.rsf
import qiniu.fop
import qiniu.rs

def tab(tabname):
    return "%s_%s" %(conf.tab_prefix, tabname)

def decode_newLine(str):
    #return str.replace('<br/>', '\n').replace('<br>', '\n').replace('<BR/>', '\n').\
    #           replace('<BR>', '\n').replace('<Br/>', '\n').replace('<Br>', '\n').replace('<bR/>', '\n').\
    #           replace('<bR>', '\n')
    return str

def encode_newLine(str):
    #return str.replace('\n', '<br/>').replace('\r\n', '<br/>')
    return str

def read_static(f):
    fileHandle = open ( f )
    cont = fileHandle.read()
    fileHandle.close()
    return cont

def get_page_dict(pageno, itemcount , pagesize=conf.page_size):
    pageno = 1 if pageno.strip() == '' else int(pageno)
    pageno = 1 if pageno < 1 else pageno
    

    pagecount = int(math.floor((itemcount + pagesize - 1) / pagesize))
    pageno = pagecount if pageno > pagecount else pageno
    
    start = (pageno - 1) * pagesize
    start = 0 if start < 0 else start
    return {"pageno": pageno, "itemcount":itemcount, "pagecount":pagecount, "start":start, "pagesize":pagesize}

def get_login():
    return web.cookies().get(conf.cookie_secure)

def vali_login():
    login_user = get_login()
    if login_user is None:
        raise web.seeother('/admin/login/')

def tag_split(tag):
    if tag is not None :
        tag = tag.strip()
        if tag == "":
            return ''
        else:
            return tag.split(',')
    else:
        return ''

def tag_implode(tags):
    if tags is None or len(tags) == 0:
        return '';
    tagss = []
    for tag in tags:
        tagss.append(tag.title)
    return ",".join(tagss)

def get_logo_img():
    import random
    return 'logo%d.jpg' %(random.randint(1, 18))

def list_all_photo(bucket,size=100, rs=None, prefix=None, limit=None):
    photos = []
    if rs is None:
        rs = qiniu.rsf.Client()
    marker = None
    err = None
    while err is None:
        ret, err = rs.list_prefix(bucket, prefix=prefix, limit=limit, marker=marker)
        marker = ret.get('marker', None)
        for item in ret['items']:
            photos.append(("http://" + conf.qiniu_domain + "/" + item['key'], get_image_preview(item['key'], size)))
            pass
    if err is not qiniu.rsf.EOF:
        # 错误处理
        pass
    return photos

def get_image_preview(name, size=100):
    iv = qiniu.fop.ImageView()
    iv.width = size

    # 生成base_url
    url = qiniu.rs.make_base_url(conf.qiniu_domain, name)
    # 生成fop_url
    url = iv.make_request(url)
    # 对其签名，生成private_url。如果是公有bucket此步可以省略
    policy = qiniu.rs.GetPolicy()
    url = policy.make_request(url)
    return url


def render_page_li(page, currentCls):
    lis = {}
    pagecount = page.pageDict['pagecount']
    cur_pageno = page.pageDict['pageno']
    if pagecount <= 13:
        for i in range(0, pagecount):
            pageno = i + 1
            page_cls = 'current' if page.pageDict['pageno'] == pageno else ''
            lis[i] = ' <li class="%s"><a href="%s%d">%d</a></li>' %(page_cls, page.get_conf('action_url'), pageno, pageno)

    else:

        ##最后一个和倒数第二个肯定是要显示的
        lis[pagecount - 3] = ' <li>...</li>'
        lis[pagecount - 2] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), pagecount-1, pagecount-1)
        lis[pagecount - 1] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), pagecount, pagecount)
        lis[pagecount] =  ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), pagecount+1, pagecount+1)

        ##前面三个
        if cur_pageno > 4:
            lis[3] = ' <li>...</li>'
            lis[2] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), 3, 3)
            lis[1] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), 2, 2)
            lis[0] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), 1, 1)
        else:
            lis[4] = ' <li>...</li>'
            lis[3] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), 4, 4)
            lis[2] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), 3, 3)
            lis[1] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), 2, 2)
            lis[0] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), 1, 1)
        ##不管怎样当前页面的前一和后一是要显示的
        if cur_pageno > 1:
            lis[cur_pageno - 2] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), cur_pageno-1, cur_pageno-1)
        lis[cur_pageno - 1] =  ' <li class="%s"><a href="%s%d">%d</a></li>' %("current", page.get_conf('action_url'), cur_pageno, cur_pageno)
        if cur_pageno < pagecount:
            lis[cur_pageno] = ' <li class="%s"><a href="%s%d">%d</a></li>' %("", page.get_conf('action_url'), cur_pageno+1, cur_pageno+1)

    lis = sorted(lis.iteritems(), key = lambda asd:asd[0])
    new_lis = []
    for (k,v) in lis:
        new_lis.append(v)
    return "".join(new_lis)

def render_page_span(page):
    pagecount = page.pageDict['pagecount']
    cur_pageno = page.pageDict['pageno']
    spans = '<a href="%s?page=1&keyword=%s">首页</a><a href="%s?page=%d&keyword=%s">上一页</a>\
            <a href="%s?page=%d&keyword=%s">下一页</a><a href="%s?page=%d&keyword=%s">尾页</a>\
            &nbsp;&nbsp;第%d/%d页&nbsp;&nbsp;每页%d条&nbsp;&nbsp;'\
     %(page.action_url,page.keyword, page.action_url,(cur_pageno-1),\
       page.keyword, page.action_url,(cur_pageno+1),\
       page.keyword, page.action_url, pagecount,page.keyword,\
       cur_pageno, pagecount,conf.page_admin_size)
    return spans

def excerpt(cont):
    if len(cont) <= conf.excerpt_size:
        return cont
    else:
        sub_cont1 = cont[0:conf.excerpt_size]
        sub_cont2 = cont[conf.excerpt_size:]
        newline_idx = sub_cont2.find('\n')
        newline_idx = len(sub_cont2) if newline_idx == -1 else newline_idx
        return cont[0:conf.excerpt_size + newline_idx]


def upload_pic_qiniu(data, filename):
    import qiniu.io

    policy = qiniu.rs.PutPolicy(conf.qiniu_bucket2)
    uptoken = policy.token()

    
    ret, err = qiniu.io.put(uptoken, filename, data)
    if err is not None:
        return False
    return True

def del_attac_qiniu(filename):
    ret, err = qiniu.rs.Client().delete(conf.qiniu_bucket2, filename)
    if err is not None:
        return False
    return True
