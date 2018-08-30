# coding=utf-8
"""
@author: kaaokou
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()  # 实例化db对象

"""定义blog模型类"""


class BaseModel(object):
    """定义数据表的基类"""
    # 将时间戳转换为指定格式time_obj.strftime("%Y-%m-%d %H:%M:%S")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    isDelete = db.Column(db.Boolean, default=False)


class BlogsCategory(db.Model, BaseModel):
    """博客分类"""
    __tablename__ = 'blogs_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    # 关联属性
    blogs = db.relationship('BlogsInfo', backref='category', lazy='dynamic')


class BlogsInfo(db.Model, BaseModel):
    """博客"""
    __tablename__ = 'blogs_info'
    id = db.Column(db.Integer, primary_key=True)
    # 定义分类外键id --> 博客分类
    category_id = db.Column(db.Integer, db.ForeignKey('blogs_category.id'))
    # 添加默认值
    pic = db.Column(db.String(50), default="blog_pic.jpg")
    title = db.Column(db.String(30))
    summary = db.Column(db.String(200))
    context = db.Column(db.Text)
    # context = db.Column(db.String(5000))

    author = db.Column(db.String(20), default='卡拗口')
    click_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    # status = db.Column(db.SmallInteger, default=1)
    # 博客与博客评论的一对多关系
    comments = db.relationship('BlogsComment', backref='blogs', lazy='dynamic', order_by='BlogsComment.id.desc()')

    @property
    def pic_url(self):
        return current_app.config.get('QINIU_URL') + self.pic


class AdminInfo(db.Model, BaseModel):
    """用户信息"""
    __tablename__ = 'admin_info'
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(50), default='header_01.jpg')
    nick_name = db.Column(db.String(20))
    # signature = db.Column(db.String(200), default="这个人很懒，什么也没留下")

    mobile = db.Column(db.String(11))
    password_hash = db.Column(db.String(200))

    # gender = db.Column(db.Boolean, default=False)

    # 用户与发布博客的一对多关系定义
    # blogs = db.relationship('blogsInfo', backref='user', lazy='dynamic')
    # 用户与评论的一对多关系定义
    # comments = db.relationship('blogsComment', backref='user', lazy='dynamic')
    # 用户与关注博客的多对多关系定义

    @property
    def password(self):
        pass

    @password.setter
    def password(self, pwd):  # 将此方法变成一个属性，加密算法
        self.password_hash = generate_password_hash(pwd)

    def check_pwd(self, pwd):  # 验证密码算法
        return check_password_hash(self.password_hash, pwd)

    @property
    def avatar_url(self):
        """七牛云获取图片地址"""
        return current_app.config.get('QINIU_URL') + self.avatar


class BlogsComment(db.Model, BaseModel):
    """博客评论"""
    __tablename__ = 'blogs_comment'
    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(20), default='游客')
    email = db.Column(db.String(20), default='youke@email.com')
    blog_address = db.Column(db.String(40), default='www.kaaokou.top')
    avatar = db.Column(db.String(50), default='header_01.jpg')

    blogs_id = db.Column(db.Integer, db.ForeignKey('blogs_info.id'))
    msg = db.Column(db.String(200))
    status = db.Column(db.SmallInteger, default=0)
    reason = db.Column(db.String(100), default='')

    # 博客评论的评论定义外键关联自身id，类似于省、市、镇关系表
    comment_id = db.Column(db.Integer, db.ForeignKey('blogs_comment.id'))
    # 博客评论与博客评论的评论自关联一对多定义
    comments = db.relationship('BlogsComment', lazy='dynamic')

    @property
    def avatar_url(self):
        """七牛云获取图片地址"""
        return current_app.config.get('QINIU_URL') + self.avatar


class BlogsMessage(db.Model, BaseModel):
    """博客评论"""
    __tablename__ = 'blogs_message'
    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(20), default='游客')
    email = db.Column(db.String(20), default='youke@email.com')
    blog_address = db.Column(db.String(40), default='www.kaaokou.top')
    avatar = db.Column(db.String(50), default='header_01.jpg')
    msg = db.Column(db.String(200))
    # 留言状态，需要审核才能显示出来
    status = db.Column(db.SmallInteger, default=0)
    reason = db.Column(db.String(100), default='')

    @property
    def avatar_url(self):
        """七牛云获取图片地址"""
        return current_app.config.get('QINIU_URL') + self.avatar
