# coding=utf-8
"""
@author: kaaokou
"""

# 创建蓝图
from datetime import datetime
from flask import Blueprint, request, session, redirect, g, render_template, current_app, jsonify

from models import AdminInfo, BlogsCategory, db, BlogsComment, BlogsMessage, BlogsInfo
from utils.rsa import get_public_key, decrypt_data

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.before_request
def before_request():
    """定义请求之前的登录验证"""
    # 1.判断是否为登录视图
    if request.path != "/admin/login":
        if "admin_id" not in session:
            return redirect("/admin/login")
        g.user = AdminInfo.query.get(session.get("admin_id"))


@admin_blueprint.route('/')
def index():
    """管理后台主页"""
    return render_template(
        "admin/index.html"
    )


@admin_blueprint.route('/login', methods=['GET', 'POST'])
def admin_login():
    """后台登录界面"""
    public_key = get_public_key(current_app.config.get("BASE_DIR"))
    if request.method == "GET":
        return render_template(
            'admin/login.html',
            public_key=public_key
        )
    elif request.method == "POST":
        dict1 = request.form
        # 1.获取用户和密码
        mobile = dict1.get("mobile")
        password = dict1.get("password")
        # 2.用户密码为空判定
        if not all([mobile, password]):
            return jsonify(result=0)
        # RSA解密
        mobile = decrypt_msg(mobile)
        password = decrypt_msg(password)
        # 3.用户是否存在
        user = AdminInfo.query.filter_by(mobile=mobile).first()
        if not user or not user.check_pwd(password):
            # 用户名或者密码错误，或者密码错误
            return jsonify(result=-1)
        # 保存用户状态
        session["admin_id"] = user.id
        return jsonify(result=1)


@admin_blueprint.route('/logout')
def admin_logout():
    """退出登录处理"""
    del session["admin_id"]
    return redirect("/admin/login")


@admin_blueprint.route('/user_count')
def user_count():
    """访问统计"""
    now = datetime.now()
    # 1.获取用户总数、月新增数和日新增数
    user_count = 1
    user_month = 1
    user_day = 1
    # 2.获取时间表以及从redis中读取用户登录记录
    now = datetime.now()
    login_log_key = "login_log:%d_%02d_%02d" % (now.year, now.month, now.day)
    # 获取所有的键值并转为字符串
    hour_list = current_app.redis_client.hkeys(login_log_key)
    hour_list = [tmp.decode() for tmp in hour_list]
    count_list = []
    for hour in hour_list:
        count_list.append(int(current_app.redis_client.hget(login_log_key, hour)))
    return render_template(
        "admin/user_count.html",
        user_count=user_count,
        user_month=user_month,
        user_day=user_day,
        hour_list=hour_list,
        count_list=count_list
    )


@admin_blueprint.route('/blog_comment_review')
def blog_comment_review():
    """blog评论审核"""
    return render_template("admin/blog_comment_review.html")


@admin_blueprint.route('/blog_comment_review_json')
def blog_comment_review_json():
    """博客评论和留言公用"""
    # 获取需要查询的页码和搜索条件
    page = int(request.args.get("page", "1"))
    input_txt = request.args.get("input_txt")
    pagination = BlogsComment.query
    if input_txt:
        # 如果有查询条件，则根据查询条件
        pagination = pagination.filter(BlogsComment.msg.contains(input_txt))
    pagination = pagination.order_by(BlogsComment.id.desc()).paginate(page, 10, False)
    # 将数据转为json格式
    comment_list = []
    for comment in pagination.items:
        blog_dict = {
            "id": comment.id,
            "msg": comment.msg,
            "create_time": comment.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": comment.status
        }
        comment_list.append(blog_dict)
    return jsonify(comment_list=comment_list, total_page=pagination.pages)


@admin_blueprint.route('/blog_comment_review_detail/<int:comment_id>', methods=['GET', 'POST'])
def blog_comment_review_detail(comment_id):
    """新闻审核详细页"""

    # 1.获取评论数据
    comment = BlogsComment.query.get(comment_id)
    if request.method == "GET":
        return render_template(
            "admin/blog_comment_review_detail.html",
            comment=comment,
        )
    elif request.method == "POST":
        # 审核提交
        action = request.form.get("action")
        reason = request.form.get("reason")
        if action == "accept":
            comment.status = 1
            comment.blogs.comment_count += 1
        elif action == "reject":
            comment.status = -1
            comment.reason = reason
        try:
            db.session.commit()
        except:
            current_app.logger_xjzx.error("审核评论提交数据库出错")
            return jsonify()
        return redirect("/admin/blog_comment_review")


@admin_blueprint.route('/blog_message_review')
def blog_message_review():
    """blog评论审核"""
    return render_template(
        "admin/blog_message_review.html"
    )


@admin_blueprint.route('/blog_message_review_json')
def blog_message_review_json():
    """博客评论和留言公用"""
    # 获取需要查询的页码和搜索条件
    page = int(request.args.get("page", "1"))
    input_txt = request.args.get("input_txt")
    pagination = BlogsMessage.query
    if input_txt:
        # 如果有查询条件，则根据查询条件
        pagination = pagination.filter(BlogsMessage.msg.contains(input_txt))
    pagination = pagination.order_by(BlogsMessage.id.desc()).paginate(page, 10, False)
    # 将数据转为json格式
    comment_list = []
    for comment in pagination.items:
        blog_dict = {
            "id": comment.id,
            "msg": comment.msg,
            "create_time": comment.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": comment.status
        }
        comment_list.append(blog_dict)
    return jsonify(comment_list=comment_list, total_page=pagination.pages)


@admin_blueprint.route('/blog_message_review_detail/<int:message_id>', methods=['GET', 'POST'])
def blog_message_review_detail(message_id):
    """blog留言审核详细页"""
    # 1.获取新闻数据
    comment = BlogsMessage.query.get(message_id)
    if request.method == "GET":
        return render_template(
            "admin/blog_message_review_detail.html",
            comment=comment,
        )
    elif request.method == "POST":
        # 审核提交
        action = request.form.get("action")
        reason = request.form.get("reason")
        if action == "accept":
            comment.status = 1
        elif action == "reject":
            comment.status = -1
            comment.reason = reason
        try:
            db.session.commit()
        except:
            current_app.logger_xjzx.error("审核评论提交数据库出错")
            return jsonify()
        return redirect("/admin/blog_message_review")


@admin_blueprint.route('/blog_edit')
def blog_edit():
    """博客编辑界面"""
    return render_template("admin/blog_edit.html")


@admin_blueprint.route('/blog_review_json')
def blog_review_json():
    """博客编辑数据接口"""
    # 获取需要查询的页码和搜索条件
    page = int(request.args.get("page", "1"))
    input_txt = request.args.get("input_txt")
    pagination = BlogsInfo.query
    if input_txt:
        # 如果有查询条件，则根据查询条件
        pagination = pagination.filter(BlogsInfo.title.contains(input_txt))
    pagination = pagination.order_by(BlogsInfo.id.desc()).paginate(page, 10, False)
    # 将数据转为json格式
    blog_list = []
    for blog in pagination.items:
        blog_dict = {
            "id": blog.id,
            "title": blog.title,
            "create_time": blog.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        blog_list.append(blog_dict)
    return jsonify(blog_list=blog_list, total_page=pagination.pages)


@admin_blueprint.route('/blog_edit_detail/<int:blog_id>', methods=['GET', 'POST'])
def blog_edit_detail(blog_id):
    """新闻审核详细页"""
    # 1.获取新闻数据
    blog = BlogsInfo.query.get(blog_id)
    category_list = BlogsCategory.query.all()
    if request.method == "GET":
        # get显示页面
        return render_template(
            "admin/blog_edit_detail.html",
            blog=blog,
            category_list=category_list,
        )
    elif request.method == "POST":
        dict1 = request.form
        title = dict1.get("title")
        category_id = int(dict1.get("category_id"))
        summary = dict1.get("summary")
        context = dict1.get("context")

        if not all([title, category_id, summary, context]):
            return jsonify()

        print(title, category_id, summary, context)
        # 图片获取方式不一样
        pic = request.files.get("pic")
        from utils.qiniu_blog import upload_pic
        blog.pic = upload_pic(pic) if pic else blog.pic
        # 编辑后的新闻赋值
        blog.title, blog.summary, blog.context = title, summary, context
        print(context)
        blog.category_id = category_id
        blog.update_time = datetime.now()
        # 提交至数据库
        try:
            db.session.commit()
        except:
            current_app.logger_blog.error("编辑新闻提交数据库出错")
            return jsonify()
        return redirect("/admin/blog_edit")


@admin_blueprint.route('/blog_issue_detail', methods=['GET', 'POST'])
def blog_issue_detail():
    """博客发布页面"""
    # 查询分类显示
    category_list = BlogsCategory.query.all()
    if request.method == "GET":
        # get显示页面
        return render_template(
            "admin/blog_issue_detail.html",
            category_list=category_list,
            blog=None
        )
    elif request.method == "POST":
        # POST表示新增
        dict1 = request.form
        title = dict1.get("title")
        category_id = int(dict1.get("category_id"))
        summary = dict1.get("summary")
        context = dict1.get("context")
        if not all([title, category_id, summary, context]):
            return jsonify()
        # 创建新的blog对象并赋值
        blog = BlogsInfo()
        # 图片获取方式不一样
        pic = request.files.get("pic")
        from utils.qiniu_blog import upload_pic
        if pic:
            blog.pic = upload_pic(pic)
        # 对blog赋值
        blog.title, blog.summary, blog.context = title, summary, context
        blog.category_id = category_id
        # 提交至数据库
        try:
            db.session.add(blog)
            db.session.commit()
        except:
            current_app.logger_blog.error("发布博客提交数据库出错")
            return jsonify()
        return redirect("/admin/blog_edit")


@admin_blueprint.route('/blog_type', methods=['GET', 'POST'])
def blog_type():
    """新闻分类管理"""
    if request.method == "GET":
        # 查询分类总数，返回
        category_list = BlogsCategory.query.all()
        return render_template(
            "admin/blog_type.html",
            category_list=category_list
        )
    elif request.method == "POST":
        # 1.获取数据
        name = request.form.get("name")
        id = int(request.form.get("id", "0"))
        action = int(request.form.get("action"))
        if not all([name, id, action]):
            return jsonify(result=0)
        # 如果name已存在，则返回
        if BlogsCategory.query.filter_by(name=name).count() > 0:
            return jsonify(result=-2)
        if action == 2:
            # 修改
            category = BlogsCategory.query.get(id)
        elif action == 1:
            # 增加
            category = BlogsCategory()
        else:
            return jsonify(result=-1)
        category.name = name
        try:
            db.session.add(category)
            db.session.commit()
        except:
            current_app.logger_xjzx.error("修改/增加分类保存数据库出错")
            return jsonify(result=-4)
        return jsonify(result=1)


@admin_blueprint.route('/blog_type_del', methods=['POST'])
def blog_type_del():
    """新闻分类管理"""
    # 1.获取数据
    category = BlogsCategory.query.get(request.form.get("id", "-1"))
    if category is None:
        return jsonify(result=-1)
    # 2.伪删除
    # category.isDelete = True
    try:
        db.session.delete(category)
        db.session.commit()
    except:
        current_app.logger_xjzx.error("删除分类保存数据库出错")
        return jsonify(result=-4)
    return jsonify(result=1)


def decrypt_msg(msg):
    """解码"""
    if msg == "":
        return None
    return decrypt_data(msg, current_app.config.get("RSA_SECRET"), current_app.config.get("BASE_DIR"))


@admin_blueprint.route('/show')
def show():
    """新闻分类管理"""
    text = '''
   
#####4. Jinja2里面使用vue需要将{{  }}替换为[[  ]]或者其他
0602-days
---
#####1.一般在什么地方是用vue
+ 在界面需要进行局部刷新并且需要实时更新数据的时候可以考虑使用这个
+ 此时需要在后台定义一个接口，提供给前端取数据

#####2.Flask中路径的习惯
+ 对于模板路径：基于templates目录进行编写，如templates/news/index.html --> 使用时路径为news/index.html，模板会自动补充前缀/templates
+ 静态文件的路径:（css,js,image）--> 存放在static/css、js、images --> 使用时路径为/static/js/index.js --> route --> /static/<filename> --> static  -->static+filename

```
def login_required(func):
    """创建一个装饰器，验证路由"""
    @functools.wraps(func)  # 返回原函数的名称，而不是装饰器内部函数名
    def inner_func(*args, **kwargs):
        if "user_id" in session:
            return func(*args, **kwargs)
        return redirect("/")  # 返回主页

    return inner_func
```

    '''
    return render_template('admin/text.html', text=text)