# coding=utf-8
"""
@author: kaaokou
"""
import os
import redis


class Config(object):
    """普通用户config配置"""
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 是否追踪
    SQLALCHEMY_DATABASE_URI = 'mysql://my_blog:XXXXXX@localhost:3306/my_blog'
    db = 3
    # redis配置
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 3  # 使用3号redis数据库
    # session 设置混淆密钥
    SECRET_KEY = "XXXX"
    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)  # 使用 redis 的实例
    PERMANENT = True  # 把这个设置为True session的有效期才有效，源码中默认为True
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 1  # session 的有效期，单位是秒，14天

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 七牛云配置 --> 未配置
    QINIU_AK = ''
    QINIU_SK = ''
    QINIU_BUCKET = ''
    QINIU_URL = ''

    # 配置RSA code
    RSA_SECRET = ''


class DevelopConfig(Config):
    """开发者config配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:XXXXX@localhost:3306/blog"  # 链接数据库


class ProductConfig(Config):
    pass
