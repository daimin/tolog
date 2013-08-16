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
    c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where `status`=1 " %(util.tab('content'))
    where_c = '`status`=1'
    if keyword is not None:
        c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where `status`=1 and `title` like '%%%s%%'" %(util.tab('content'), keyword)
        where_c = "`status`=1 and `title` like '%%%s%%'" % (keyword)

    results = db.query(c_sql)
    count =  results[0].cid
    pageDict = util.get_page_dict(pageno, count)
    return (db.select(util.tab('content'),where=where_c, order='`id` DESC', limit=pageDict['pagesize'], offset=pageDict['start']), pageDict )

def get_admin_posts(pageno, keyword=None):
    c_sql = "SELECT COUNT(`id`) AS cid FROM `%s`" %(util.tab('content'))
    where_c = '1=1'
    if keyword is not None and keyword <> '':
        c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where `title` like '%%%s%%' or `createtime` like '%%%s%%' or `modifytime` like '%%%s%%'"\
         %(util.tab('content'), keyword, keyword, keyword)
        where_c = "`title` like '%%%s%%' or `createtime` like '%%%s%%' or `modifytime` like '%%%s%%'" % (keyword, keyword, keyword)

    results = db.query(c_sql)
    count =  results[0].cid
    pageDict = util.get_page_dict(pageno, count, conf.page_admin_size)
    return (db.select(util.tab('content'),where=where_c, order='`id` DESC', limit=pageDict['pagesize'], offset=pageDict['start']), pageDict )

##根据创建时间得到文档
def get_posts_by_createtime(pageno, date=None, month=None, year=None, arch=None):
    c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where `status`=1" %(util.tab('content'))
    where_c = '`status`=1'
    if date is not None:
        c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where `status`=1 and DATE_FORMAT(createtime, '%%d')='%s'" %(util.tab('content'), date)
        where_c = "`status`=1 and DATE_FORMAT(createtime, '%%d')='%s' " % (date)
    elif month is not None:
        c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where `status`=1 and DATE_FORMAT(createtime, '%%m')='%s'" %(util.tab('content'), month)
        where_c = "`status`=1 and DATE_FORMAT(createtime, '%%m')='%s' " % (month)
    elif year is not None:
        c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where `status`=1 and DATE_FORMAT(createtime, '%%Y')='%s'" %(util.tab('content'), year)
        where_c = "`status`=1 and DATE_FORMAT(createtime, '%%Y')='%s' " % (year)
    elif arch is not None:
        c_sql = "SELECT COUNT(`id`) AS cid FROM `%s` where `status`=1 and DATE_FORMAT(createtime, '%%Y-%%m')='%s'" %(util.tab('content'), arch)
        where_c = "`status`=1 and DATE_FORMAT(createtime, '%%Y-%%m')='%s' " % (arch)

    results = db.query(c_sql)
    count =  results[0].cid
    pageDict = util.get_page_dict(pageno, count)
    return (db.select(util.tab('content'),where=where_c, order='`id` DESC', limit=pageDict['pagesize'], offset=pageDict['start']), pageDict )

##得到最新的文档列表
def get_recent_posts():
    return db.select(util.tab('content'),where='`status`=1', order='`createtime` DESC', limit=conf.list_size, offset=0)

##得到随机的文档列表
def get_rand_posts():
    return db.select(util.tab('content'),where='`status`=1', order='RAND()', limit=conf.list_size, offset=0)


def get_posts_by_tag(tagid, pageno):
    myvars = dict(tid=tagid)
    tags = db.select(util.tab('metas'), myvars, where="`id`=$tid")
    tag = None
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

            return (db.select(util.tab('content'), where="`status`=1 and `id` in (%s)" %(cids), order='`id` DESC', limit=pageDict['pagesize'], offset=pageDict['start']),pageDict,tag )
    return ([], None, tag)

    count =  results[0].cid
    pageDict = util.get_page_dict(pageno, count)
    return (db.select(util.tab('content'), where="`status`=1", order='`id` DESC', limit=pageDict['pagesize'], offset=pageDict['start']),pageDict, tag )

def get_post(id):
    try:

        post =  db.select(util.tab('content'), where='id=$id', vars=locals())[0]
        post.attacs = get_attac_post(post.id)

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
    
def get_attac_post(postid):
    rels =  db.select(util.tab('attac_rel'), where='rel_id=$postid', vars=locals())
    
    attacs = []
    for rel in rels:
        attac = db.select(util.tab('attac'), where='id=%s' % (rel.att_id))
        if attac is not None and len(attac) > 0:
            attacs.append(attac[0])
    return attacs

def new_post(title, text, tag, isMd, st, attacs):
    ctime = datetime.datetime.utcnow()
    mtime = ctime
    insert_id = db.insert(util.tab('content'), title=title, content=text, \
             createtime=ctime, modifytime=mtime, is_md=1, status=st)
    if insert_id is not None:
        add_tag(insert_id, tag)
        add_attacs(insert_id, attacs)

def add_attacs(post_id, attacs):
    attacs = attacs.split("|")
    if attacs is not None and len(attacs) > 0:
        for attac in attacs:
            if attac is not None:
                attac = attac.strip()
                try:
                    attac = int(attac)
                    db.insert(util.tab('attac_rel'), att_id=attac, rel_id=post_id)
                except:
                    continue;
                    
    #删除一下没有post关联的附件
    #这里还要删文件啊
    s_sql = "select * from `%s` where id not in(select att_id from `%s`)" %(util.tab('attac'), util.tab('attac_rel'))
    result = db.query(s_sql)
    if result is not None and len(result) > 0:
        for res in result:
            util.del_attac_qiniu(res.title)
        d_sql = "delete from `%s` where id not in(select att_id from `%s`)" %(util.tab('attac'), util.tab('attac_rel'))
        db.query(d_sql)

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

def get_tags():
    tags = db.query("select id,title from `%s` where `type`='tag' \
                     order by RAND() limit 64" %(util.tab("metas")))
    ctags = []
    for tag in tags:
        rel = db.query("select count(cid) as ccount from `%s` where mid='%d'"\
                       %(util.tab("rel"), tag.id))
        if rel is not None and len(rel) > 0:
            ctags.append({'id':tag.id, 'title':tag.title,'count':rel[0].ccount})
    return ctags

def get_tags_admin():
    tags = db.query("select id,title from `%s` where `type`='tag' \
                     order by id" %(util.tab("metas")))
    ctags = []
    for tag in tags:
        rel = db.query("select count(cid) as ccount from `%s` where mid='%d'"\
                       %(util.tab("rel"), tag.id))
        if rel is not None and len(rel) > 0:
            ctags.append({'id':tag.id, 'title':tag.title,'count':rel[0].ccount})
    return ctags

def get_archives():
    c_sql = u"SELECT COUNT(id) AS cid, DATE_FORMAT(createtime, '%%Y-%%m')\
            AS month_arch FROM `%s` where `status`=1 GROUP BY month_arch\
             ORDER BY month_arch DESC LIMIT %d" %(util.tab("content"), conf.list_size)
    result = db.query(c_sql)
    if result is not None and len(result) > 0:
        return result
    return None



def del_tag(post_id):
    myvars = dict(cid=post_id)
    db.delete(util.tab('rel'),where="cid=$cid",vars=myvars)
    
def del_tag_id(tid):
    myvars = dict(tid=tid)
    db.delete(util.tab('metas'),where="id=$tid",vars=myvars)
    db.delete(util.tab('rel'),where="mid=$tid",vars=myvars)
    
def del_attac(post_id):
    myvars = dict(rel_id=post_id)
    db.delete(util.tab('attac_rel'),where="rel_id=$rel_id", vars=myvars)

def del_post(id):
    #这里还需要删所有的关联
    #删除附件关联
    myvars = dict(rel_id=id)
    db.delete(util.tab('attac_rel'), where="rel_id=$rel_id", vars=myvars)
    #删除meta关联
    myvars = dict(cid=id)
    db.delete(util.tab('rel'), where="cid=$cid", vars=myvars)
    
    myvars = dict(id=id)
    db.delete(util.tab('content'), where="id=$id", vars=myvars)

def get_attac_id(id):
    try:
        return db.select(util.tab('attac'), where="id=$id", vars=locals())[0]
    except IndexError:
        return None

def del_attac_aid(id):
    #这里也是要删关联
    myvars = dict(att_id=id)
    db.delete(util.tab('attac_rel'), where="att_id=$att_id", vars=myvars)
    myvars = dict(id=id)
    #还要删文件
    attac = get_attac_id(id)
    if attac is not None:
        util.del_attac_qiniu(attac.title)
        db.delete(util.tab('attac'), where="id=$id", vars=myvars)
    
    

def update_post(id, title, text, tag, st, attacs):
    mtime = datetime.datetime.utcnow()

    db.update(util.tab('content'), where="id=$id", vars=locals(),
        title=title, content=text,createtime=mtime, status=st)
    del_tag(id)
    add_tag(id, tag)
    del_attac(id)
    add_attacs(id, attacs)

def update_view_num(post_id):
    db.query("update `%s` set view_num=view_num+1 where `id`='%d'" % (util.tab('content'),post_id))

def get_password_by_name(user):
    try:
        return db.select(util.tab('admin'), where="username='%s'" %(user))[0]
    except IndexError:
        return None
    
def save_attac(name):
    ctime = datetime.datetime.utcnow()
    url = conf.qiniu_domain2 + '/' + name
    insert_id = db.insert(util.tab('attac'), title=name, path=url, \
             createtime=ctime)
    return [insert_id,url]
