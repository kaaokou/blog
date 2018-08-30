# coding=utf-8
"""
@author: kaaokou
"""
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from config import DevelopConfig
from models import db
from script_command import SuperAdminCommand,CreateRequest
from utils.rsa import create_rsa_key

app = create_app(DevelopConfig)
db.init_app(app)  # 初始化

if __name__ == '__main__':
    """程序主入口"""
    # 创建manager管理对象
    manager = Manager(app)
    db.init_app(app)  # 初始化

    # 创建迁移
    Migrate(app, db)

    # 添加扩展命令
    manager.add_command('db', MigrateCommand)
    manager.add_command('create_admin', SuperAdminCommand)
    manager.add_command('create_request', CreateRequest)

    # 创建密钥
    create_rsa_key(app.config.get("RSA_SECRET"), app.config.get("BASE_DIR"))

    manager.run()  # 启动项目
    # app.run(port=8080)  # 启动项目

