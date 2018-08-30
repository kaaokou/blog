# coding=utf-8
"""
@author: kaaokou
"""
import random
from datetime import datetime

from flask import current_app
from flask_script import Command

from models import AdminInfo, db


class SuperAdminCommand(Command):
    """创建管理员类"""

    def run(self):
        """重写的run方法"""
        mobile = input("请输入管理员用户名：")
        pwd = input("请输入管理员密码：")
        if AdminInfo.query.filter_by(mobile=mobile).count() > 0:
            print("管理员%s已存在" % mobile)
            return
        user = AdminInfo()
        user.mobile = mobile
        user.nick_name = mobile
        user.password = pwd
        user.isAdmin = True
        try:
            db.session.add(user)
            db.session.commit()
        except:
            print("创建管理员用户失败")
            return
        print("管理员用户创建成功")


class CreateRequest(Command):
    """创建请求情况"""

    def run(self):
        now = datetime.now()
        day_key = "login_log:%d_%02d_%02d" % (now.year, now.month, now.day)
        for day in range(8, 20):
            current_app.redis_client.hset(day_key, "%02d:15" % day, random.randint(200, 1000))
        print("创建访问数据完成")
