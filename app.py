# coding=utf-8
"""
@author: kaaokou
"""
import re

from flask import Flask, render_template, session
from flask_session import Session

from views_admin import admin_blueprint
from views_blog import blog_blueprint
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler


def create_app(Config):
    """创建和配置app"""
    app = Flask(__name__)

    # 配置app
    app.config.from_object(Config)

    # 注册蓝图
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(admin_blueprint)

    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler(Config.BASE_DIR + "/logs/my_blog.log", maxBytes=1024 * 1024 * 100,
                                           backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
    app.logger_blog = logging

    # 定义redis_client属性
    from redis import StrictRedis  # 导入模块
    host = app.config.get('REDIS_HOST')
    port = app.config.get('REDIS_PORT')
    redis_db = app.config.get('REDIS_DB')
    app.redis_client = StrictRedis(host=host, port=port, db=redis_db)

    # 防止csrf攻击
    CSRFProtect(app)
    # Session设置
    Session(app)

    # 捕获异常处理 页面不存在返回404
    @app.errorhandler(404)
    def error_handler_404(e):
        """处理404异常"""
        return '---not--found--page--404---'

    # 定义md过滤器
    @app.template_filter('md')
    def markdown_to_html(txt):
        from markdown import markdown
        # 将txt提取为纯文本
        # pattern = r"<[^>]*>|\s"
        # txt = re.sub(pattern, '\n', txt)
        return markdown(txt, ['extra', 'codehilite'])
    return app
