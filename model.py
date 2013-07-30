# -*- coding:utf-8 -*-
# encoding: utf-8

import web, datetime
import conf
import util
#import log

#logger = log.getlogger()

db = web.database(dbn=conf.db['dbn'], db=conf.db['dbname'], 
                  user=conf.db['user'], passwd=conf.db['password'],
                  host=conf.db['host'], port=conf.db['port'])

def get_posts(pageno, keyword=None):
    c_sql = "SELECT COUNT(`id`) AS cid FROM `%s`" %(util.tab('content'))
    where_c = '1=1'
    if keyword is not None:
        c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where `title` like '%%%s%%'" %(util.tab('content'), keyword)
        where_c = "`title` like '%%%s%%'" % (keyword)
    
    results = db.query(c_sql)
    count =  results[0].cid
    pageDict = util.get_page_dict(pageno, count)
    return (db.select(util.tab('content'),where=where_c, order='`id` DESC', limit=pageDict['pagesize'], offset=pageDict['start']), pageDict )

def get_posts_by_createtime(pageno, date=None, month=None, year=None):
    c_sql = "SELECT COUNT(`id`) AS cid FROM `%s`" %(util.tab('content'))
    where_c = '1=1'
    if date is not None:
        c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where DATE_FORMAT(createtime, '%%d')=%s" %(util.tab('content'), date)
        where_c = " DATE_FORMAT(createtime, '%%d')=%s " % (date)
    elif month is not None:
        c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where DATE_FORMAT(createtime, '%%m')=%s" %(util.tab('content'), month)
        where_c = " DATE_FORMAT(createtime, '%%m')=%s " % (month)
    elif year is not None:
        c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where DATE_FORMAT(createtime, '%%Y')=%s" %(util.tab('content'), year)
        where_c = " DATE_FORMAT(createtime, '%%Y')=%s " % (year)
    
    results = db.query(c_sql)
    count =  results[0].cid
    pageDict = util.get_page_dict(pageno, count)
    return (db.select(util.tab('content'),where=where_c, order='`id` DESC', limit=pageDict['pagesize'], offset=pageDict['start']), pageDict )

def get_posts_by_tag(tag, pageno):
    myvars = dict(tid=tag)
    tags = db.select(util.tab('metas'), myvars, where="`id`=$tid")
    if tags is not None and len(tags) > 0:
        tag = tags[0]
        results = db.query("SELECT COUNT(`cid`) AS countc FROM `%s` where `mid`='%d'" %(util.tab('rel'), tag.id))
        if results is not None and len(results) > 0:
            countc = results[0].countc
            pageDict = util.get_page_dict(pageno, countc)
            rels = db.select(util.tab('rel'),myvars, where="`mid`=$tid", order='`cid` DESC', limit=pageDict['pagesize'], offset=pageDict['start'])
            
            cids = []
            for rel in rels:
                cids.append(str(rel.cid))
            cids = ",".join(cids)
            
            return (db.select(util.tab('content'), where="`id` in (%s)" %(cids), order='`id` DESC', limit=pageDict['pagesize'], offset=pageDict['start']),pageDict )
    return ([], None)       
    
    count =  results[0].cid
    pageDict = util.get_page_dict(pageno, count)
    return (db.select(util.tab('content'), order='`id` DESC', limit=pageDict['pagesize'], offset=pageDict['start']),pageDict )

def get_post(id):
    try:
        
        post =  db.select(util.tab('content'), where='id=$id', vars=locals())[0]
        
        #获取上一篇和下一篇,是否有比当前文档的ID大和小的文章，有就返回
        myvars = dict(pid=post.id)
        prev_post = db.select(util.tab('content'),myvars, where="`id`<$pid", order="`id` desc", limit=1)
        if prev_post is not None and len(prev_post) > 0:
            prev_post = prev_post[0]
        else:
            prev_post = None
            
        next_post = db.select(util.tab('content'),myvars, where="`id`>$pid", order="`id` asc", limit=1)
        if next_post is not None and len(next_post) > 0:
            next_post = next_post[0]
        else:
            next_post = None
        return (post, prev_post, next_post)
    except IndexError:
        return None

def new_post(title, text, tag, isMd):
    ctime = datetime.datetime.utcnow()
    mtime = ctime
    insert_id = db.insert(util.tab('content'), title=title, content=text, createtime=ctime, modifytime=mtime, is_md=1)
    if insert_id is not None:
        add_tag(insert_id, tag)
                    

def add_tag(post_id, tag):
    
    tags = util.tag_split(tag)
    
    if tags != '':
        for tag in tags:
            myvars = dict(title=tag)
            metas = db.select(util.tab('metas'), myvars, where="`type`='tag' and `title`=$title")
            
            has_tag = False
            if metas is not None and len(metas) > 0:
                    has_tag = True
            if has_tag is False:
                tag_id = db.insert(util.tab('metas'), title=tag, type='tag')
            else:
                tag_id = metas[0].id
            db.query("replace into `%s`(cid,mid) values('%d','%d')" % (util.tab('rel'),post_id,tag_id ))
            
def get_tag(post_id):
    myvars = dict(cid=post_id)
    rels = db.select(util.tab('rel'), myvars, where="`cid`=$cid")
    tags = []
    for rel in rels:
        myvars = dict(mid=rel.mid)
        tag = db.select(util.tab('metas'), myvars, where="`id`=$mid")
        if tag is not None and len(tag) > 0:
            tags.append(tag[0])
    return tags

def del_tag(post_id):
    myvars = dict(cid=post_id)
    db.delete(util.tab('rel'),where="cid=$cid",vars=myvars)

def del_post(id):
    db.delete(util.tab('content'), where="id=$id", vars=locals())

def update_post(id, title, text, tag):
    mtime = datetime.datetime.utcnow()
    
    db.update(util.tab('content'), where="id=$id", vars=locals(),
        title=title, content=text,createtime=mtime)
    del_tag(id)
    add_tag(id, tag)
    
def update_view_num(post_id):
    db.query("update `%s` set view_num=view_num+1 where `id`='%d'" % (util.tab('content'),post_id))
    
def get_password_by_name(user):
    try:
        return db.select(util.tab('admin'), where="username='%s'" %(user))[0]
    except IndexError:
        return None
    