# -*- coding: utf-8 -*-
from Blog.common.basehandler import BaseHandler
from Blog.common.dbhandler import DBHandler,DBsession
from Blog.common.pagination import PaginationHandler
from models import Article,Comment,Category,Tag,Lognote,Weblink,UploadFile,Article_Tag
from Blog.user.usermodel import User
from uuid import uuid4
import tornado.web
import json,datetime
from sqlalchemy import and_, or_
from sqlalchemy.sql import func
from sqlalchemy import distinct

def get_newestcommnet_article():
    """
    获取最新评论文章
    """
    comment_article =DBHandler(Comment,Comment.article_id).dist()
    com_art_list=[]
    for com_art in comment_article:
        com_art_list.append(com_art[0])  
    comment_article=DBHandler(Article,Article.id).filter_in(*com_art_list)
    categroy_obj=DBHandler(Category).query()
    return comment_article,categroy_obj

class IndexHandler(BaseHandler):
    """
       *首页页面处理*
    """
    def get(self,categroy):

        category_count=DBHandler(Article,Article.category_id).count()
        article_obj=DBHandler(Article,column1=Article.date).order_desc()
        comment_article,categroy_obj=get_newestcommnet_article()
        article_all=None
        if 'index' in categroy:
            article_all=article_obj.all()
        elif 'search' in categroy:
            keyword=self.get_argument('keyword')
            article_all=DBsession.query(Article).filter(or_(Article.title.like('%'+keyword+'%'), Article.brief.like('%'+keyword+'%'))).all() if keyword else None
        for cate in categroy_obj:
            if cate.urlname in categroy:
                article_all = article_obj.filter(Article.category_id == cate.id).all()
        if not article_all:
            self.render('404.html')
        current_page=int(categroy.split('-')[1]) if '-' in categroy else 1
        pagination=PaginationHandler(current_page,len(article_all))
        pager_html=pagination.render(categroy.split('-')[0]) if 'search' not in categroy else  pagination.render(categroy.split('-')[0],kw='?keyword=%s'%keyword)
        article_all=article_all[pagination.start:pagination.end]
        self.render('index.html',articleobjs=article_all,category_count=category_count,category_objs=categroy_obj,pagination=pager_html,comment_article=comment_article)

class MainHandler(BaseHandler):
    '''
    *首页/跳转*
    '''
    def get(self):
        self.redirect('index/index.html')

class ShowDetailHandler(BaseHandler):
    """
       *文章详细页面处理*
    """
    def get(self,blogname,aid):
        comment_objs=DBHandler(Comment,Comment.article_id).query(aid)
        user_obj=DBHandler(User,User.name).query(blogname)[0]
        category_count = DBHandler(Article, Article.category_id, Article.user_id).self_count(user_obj.id)
        comment_article,categroy_obj=get_newestcommnet_article()
        for cate in categroy_obj:
            if cate.urlname in aid:
                current_page = int(aid.split('-')[1]) if '-' in aid else 1
                blogname=aid.split('-')[0]
                article_all = DBsession.query(Article).filter(and_(Article.user_id==user_obj.id, Article.category_id==cate.id)).order_by(Article.page_views.desc()).all()#DBHandler(Article,Article.user_id).query(user_obj.id).filter(Article.category_id == cate.id).all()
                pagination = PaginationHandler(current_page, len(article_all))
                pager_html = pagination.render(blogname)
                article_all = article_all[pagination.start:pagination.end]
                self.render('myblog.html', articleobjs=article_all, category_objs=categroy_obj,category_count=category_count,user_obj=user_obj,comment_article=comment_article,pagination=pager_html)
        else:
            article_obj = DBHandler(Article,Article.id).query(aid)
            if article_obj:
                article_obj[0].page_views+=1
                DBHandler(Article).commit()
                self.render('showdetail.html',articleobj=article_obj[0],commentobjs=comment_objs,category_count=category_count,category_objs=categroy_obj,user_obj=user_obj,comment_article=comment_article)
            else:
                self.render('404.html')
class ShowLognoteHandler(BaseHandler):
    def get(self,blogname,lid):
        comment_objs=DBHandler(Comment,Comment.article_id).query(lid)
        #categroy_obj = DBHandler(Category).query()
        user_obj=DBHandler(User,User.name).query(blogname)[0]
        #category_count = DBHandler(Article, Article.category_id, Article.user_id).self_count(user_obj.id)
        #comment_article=DBHandler(Comment,Comment.date).order_desc()
        lognote_obj=DBHandler(Lognote,Lognote.id).query(lid)
        if lognote_obj:
            self.render('showdetail.html',articleobj=lognote_obj[0],commentobjs=comment_objs,category_count=category_count,category_objs=categroy_obj,user_obj=user_obj)#,comment_article=comment_article)
        else:
            self.render('404.html')

class CommentHandler(BaseHandler):
    """
       *评论页面处理*
       """
    @tornado.web.authenticated
    def post(self):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content=self.get_argument('content')
        userid=self.get_argument('userid')
        articleid=self.get_argument('articleid')
        new_comment=Comment(id=str(uuid4()),content=content,article_id=articleid,user_id=userid)
        DBHandler(new_comment).add()
        data={'status':'ok','username':self.current_user.name,'date':current_time}
        self.write(data)

class SelfBlogHandler(BaseHandler):
    '''
    *展示自己的博客*
    '''
    def get(self,blogname):

        if blogname.lower()=='index':
            self.redirect('index/index.html')
        current_page=int(blogname.split('-')[1]) if '-' in blogname else 1
        if '-' in blogname:
            blogname = blogname.split('-')[0]
        user_obj=DBHandler(User,User.name).query(blogname)[0]
        article_all=DBsession.query(Article).filter(Article.user_id==user_obj.id).order_by(Article.page_views.desc()).all()
        category_count =DBHandler(Article,Article.category_id,Article.user_id).self_count(user_obj.id)
        comment_article,categroy_obj=get_newestcommnet_article()
        keyword = self.get_argument('keyword','')
        if keyword:
            article_all = DBsession.query(Article).filter(Article.user_id==user_obj.id).filter(or_(Article.title.like('%' + keyword + '%'), Article.brief.like( '%' + keyword + '%'))).order_by(Article.page_views.desc()).all() if keyword else None
            if len(article_all)<1:
                self.render('404.html')
        pagination = PaginationHandler(current_page, len(article_all))
        pager_html = pagination.render(blogname) if 'search' not in blogname else  pagination.render(blogname.split('-')[0], kw='?keyword=%s' % keyword)
        article_all = article_all[pagination.start:pagination.end]
        self.render('myblog.html',articleobjs=article_all,category_objs=categroy_obj,category_count=category_count,pagination=pager_html,user_obj=user_obj,comment_article=comment_article)

class BackendHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,backendkey):
        article_objs = DBHandler(Article, Article.user_id, Article.date).order_desc(self.current_user.id).all()
        if backendkey == "index":
            article_num=len(DBHandler(Article,Article.user_id).query(self.current_user.id))
            lognote_num=len(DBHandler(Lognote,Lognote.user_id).query(self.current_user.id))
            comment_num=len(DBHandler(Comment,Comment.user_id).query(self.current_user.id))
            return self.render('backend.html',article_num=article_num,lognote_num=lognote_num,comment_num=comment_num)
        elif  'article'in backendkey  :
            if self.get_argument('delid',''):
                DBHandler(Comment, Comment.article_id).delete(self.get_argument('delid',''))
                DBHandler(Article_Tag, Article_Tag.article_id).delete(self.get_argument('delid',''))
                DBHandler(Article,Article.id).delete(self.get_argument('delid',''))
            article_objs = DBHandler(Article, Article.user_id,Article.date).order_desc(self.current_user.id).all()#DBHandler(Article, Article.user_id).query(self.current_user.id)
        elif "lognote" in backendkey:
            if self.get_argument('delid',''):
                DBHandler(Lognote, Lognote.id).delete(self.get_argument('delid',''))
            article_objs = DBHandler(Lognote, Lognote.user_id,Lognote.date).order_desc(self.current_user.id).all()
        elif "weblink" in backendkey:
            if self.get_argument('delid',''):
                DBHandler(Weblink, Weblink.id).delete(self.get_argument('delid',''))
            article_objs = DBHandler(Weblink, Weblink.user_id,Weblink.date).order_desc(self.current_user.id).all()
        elif "uploadfile" in backendkey:
            article_objs = DBHandler(UploadFile,UploadFile.user_id,UploadFile.date).order_desc(self.current_user.id).all()
        current_page = int(backendkey.split('-')[1]) if '-' in backendkey else 1
        if '-' in backendkey:
            backendkey = backendkey.split('-')[0]
        pagination = PaginationHandler(current_page, len(article_objs),per_page_count=20)
        pager_html = pagination.render(backendkey)
        article_objs = article_objs[pagination.start:pagination.end]
        self.render('backend_list.html', articleobjs=article_objs,pagination=pager_html,msg="")

class BackendEditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,editkey):
        category_obj = DBHandler(Category).query()
        tag_obj = DBHandler(Tag).query()
        edit_obj=None
        if editkey == 'article':
            if self.get_argument('editid',''):
                edit_obj=DBHandler(Article, Article.id).query(self.get_argument('editid',''))[0]
        elif editkey == 'lognote':
            if self.get_argument('editid', ''):
                edit_obj = DBHandler(Lognote, Lognote.id).query(self.get_argument('editid', ''))[0]
        elif editkey == 'weblink':
            if self.get_argument('editid',''):
                edit_obj=DBHandler(Weblink, Weblink.id).query(self.get_argument('editid',''))[0]
        self.render('backend_edit.html',category_obj=category_obj,tag_obj=tag_obj,edit_obj=edit_obj)

    @tornado.web.authenticated
    def post(self, editkey):

        title = self.get_argument('title', '')
        brief = self.get_argument('brief', '')
        content1 = self.get_argument('content','')
        description=content = self.get_argument('description', '')
        category = self.get_argument('category', '')
        tags=self.get_body_arguments('tag','')
        if editkey == 'article':
            if self.get_argument('editid', ''):
                new_article = DBHandler(Article,Article.id).update(self.get_argument('editid', ''),title=title,brief=brief,content=content1,category_id=category)
                DBHandler(Article_Tag, Article_Tag.article_id).delete(self.get_argument('editid',''))
                if tags:
                    for tag in tags:
                        new_article_tag=Article_Tag(article_id=self.get_argument('editid', ''),tag_id=tag)
                        DBHandler(new_article_tag).add() 
            else:
                new_article=Article(id=str(uuid4()),title=title,brief=brief,content=content1,category_id=category,user_id=self.current_user.id)
                if tags:
                    tag_obj=DBHandler(Tag,Tag.id).query(tags[0])[0]
                    images='images/%s.png'%tag_obj.name.lower()
                    new_article.image=images
                DBHandler(new_article).add()
                if tags:
                    for tag in tags:
                        new_article_tag=Article_Tag(article_id=new_article.id,tag_id=tag)
                        DBHandler(new_article_tag).add()         
        elif editkey == 'lognote':
            if self.get_argument('editid', ''):
                new_article = DBHandler(Lognote,Lognote.id).update(self.get_argument('editid', ''),title=title,brief=brief,content=content1)
            else:
                new_lognote=Lognote(title=title,brief=brief, content=content1, user_id=self.current_user.id)
                DBHandler(new_lognote).add()
        elif editkey == 'weblink':
            if self.get_argument('editid', ''):
                new_article = DBHandler(Weblink,Weblink.id).update(self.get_argument('editid', ''),title=title, weburl=brief, description=description)
            else:
                new_weblink = Weblink(title=title, weburl=brief, description=description,user_id=self.current_user.id)
                DBHandler(new_weblink).add()

        self.redirect('/backend/%s.html'%editkey)




