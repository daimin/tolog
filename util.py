# -*- coding:utf-8 -*-
# encoding: utf-8
import conf
import math
import web

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

def get_page_dict(pageno, itemcount):
    pageno = 1 if pageno.strip() == '' else int(pageno)
    pageno = 1 if pageno < 1 else pageno
    
    pagecount = int(math.floor((itemcount + conf.page_size - 1) / conf.page_size))
    start = (pageno - 1) * conf.page_size
    
    return {"pageno": pageno, "itemcount":itemcount, "pagecount":pagecount, "start":start, "pagesize":conf.page_size}

def get_login():
    return web.cookies().get(conf.cookie_secure)

def vali_login():
    login_user = get_login()
    if login_user is None:
        raise web.seeother('/login')

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


