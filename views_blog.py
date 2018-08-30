# coding=utf-8
"""
@author: kaaokou
"""

# 创建蓝图
import functools

from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, current_app, session

from models import BlogsMessage, db, BlogsInfo, BlogsCategory, BlogsComment

blog_blueprint = Blueprint('blog', __name__, url_prefix='')


@blog_blueprint.before_request
def befroe_request():
    """每次请求让访问量+1"""
    now = datetime.now()
    login_log_key = 'login_log:%d_%02d_%02d' % (now.year, now.month, now.day)
    login_prop = ['08:15', '09:15', '10:15', '11:15', '12:15', '13:15', '14:15', '15:15', '16:15', '17:15', '18:15',
                  '19:15']
    # 判定是否需要往前挪一位
    index = now.hour - 8 + (1 if now.minute > 15 else 0)
    # 对index做截断处理使其满足 0<=index<=11
    index = 0 if index < 0 else (index if index < 11 else 11)
    # 1.获取数据
    count = current_app.redis_client.hget(login_log_key, login_prop[index])
    count = (int(count) + 1) if count else 1

    # 2.写入数据
    current_app.redis_client.hset(login_log_key, login_prop[index], count)


@blog_blueprint.route('/')
def index():
    """blog主页视图"""
    return render_template('blog/index.html', title='卡拗口的博客')


@blog_blueprint.route('/detail_list')
def detail_list():
    """文章列表页"""
    # 查询分类的栏目
    category_list = BlogsCategory.query.all()
    # 查询热门文章及分类，向后台显示
    rank_blogs = BlogsInfo.query.order_by(BlogsInfo.click_count.desc())[0:5]

    return render_template(
        'blog/detail_list.html',
        title='文章 | 卡拗口的博客',
        category_list=category_list,
        rank_blogs=rank_blogs
    )


@blog_blueprint.route('/get_detail_list')
def get_detail_list():
    """获取blog列表"""
    # 1.查询blog数据
    page = int(request.args.get('page', '1'))
    category_id = int(request.args.get('category_id', '0'))
    # 2.分页查询数据
    pagination = BlogsInfo.query
    if category_id:
        pagination = pagination.filter_by(isDelete=False, category_id=category_id)
    else:
        pagination = pagination.filter_by(isDelete=False)
    pagination = pagination.order_by(BlogsInfo.id.desc()).paginate(page, 4, False)

    blog_list = []
    # 3.转换为JSON数据
    for blog in pagination.items:
        blog_dict = {
            'id': blog.id,
            'pic_url': blog.pic_url,
            'title': blog.title,
            'summary': blog.summary,
            'author': blog.author,
            'category': blog.category.name,
            'click_count': blog.click_count,
            'comment_count': blog.comment_count,
            'year': blog.create_time.strftime("%Y"),
            'month': blog.create_time.strftime('%b'),
            'day': blog.create_time.strftime("%d"),

        }
        blog_list.append(blog_dict)
    return jsonify(
        blog_list=blog_list,
        page=page,
    )


@blog_blueprint.route('/search_detail_list')
def search_detail_list():
    """获取搜索的blog"""
    # 1.获取搜索的关键字
    search_name = request.args.get('search_name')
    print(search_name)
    if not search_name:
        return jsonify(result=0)
    # 2.查询blog数据
    page = int(request.args.get('page', '1'))
    # 3.分页查询数据
    pagination = BlogsInfo.query.filter_by(isDelete=False)
    pagination = pagination.filter(BlogsInfo.title.contains(search_name))
    pagination = pagination.order_by(BlogsInfo.id.desc()).paginate(page, 4, False)

    blog_list = []
    # 3.转换为JSON数据
    for blog in pagination.items:
        blog_dict = {
            'id': blog.id,
            'pic_url': blog.pic_url,
            'title': blog.title,
            'summary': blog.summary,
            'author': blog.author,
            'category': blog.category.name,
            'click_count': blog.click_count,
            'comment_count': blog.comment_count,
            'year': blog.create_time.strftime("%Y"),
            'month': blog.create_time.strftime('%b'),
            'day': blog.create_time.strftime("%d"),

        }
        blog_list.append(blog_dict)
    return jsonify(
        blog_list=blog_list,
        page=page,
    )


@blog_blueprint.route('/detail/<int:blog_id>')
def detail(blog_id):
    """文章详细页"""
    # 查询blog
    blog = BlogsInfo.query.get(blog_id)
    if not blog:
        return '---页面未找到----'
    # 动态增加访问次数，获取访问的ip地址
    ip = request.remote_addr
    # 检查ip是否在session中
    key = 'ip_list_%d' % blog_id
    ip_list = session.get(key, [])
    if ip not in ip_list:
        # 不再则添加
        ip_list.append(ip)
        session[key] = ip_list
        blog.click_count += 1
        try:
            db.session.commit()
        except:
            current_app.logger_blog.error('新增访问量访问数据库失败')
            return '---页面未找到----'

    return render_template(
        'blog/detail.html',
        title=blog.title,
        blog=blog,
    )


@blog_blueprint.route('/get_comment_list/<int:blog_id>')
def get_comment_list(blog_id):
    """评论数据接口，vue请求留言数据"""
    # 1.查询blog
    blog = BlogsInfo.query.get(blog_id)
    if not blog:
        return jsonify(result=-1)
    # 2.查询留言的数据
    page = int(request.args.get('page', '1'))
    # 3.分页查询数据
    blog_comments = BlogsComment.query.filter_by(comment_id=None, blogs_id=blog_id, status=1). \
        order_by(BlogsComment.id.asc()).paginate(page, 4, False)

    # 4.装换数据为JSON
    comment_list = []
    # 获取当前用户存储在redis的点赞评论列表 --> comment_up_list
    for comment in blog_comments.items:
        comment_dict = {
            "id": comment.id,
            'avatar': comment.avatar_url,
            'nick_name': comment.nick_name,
            'msg': comment.msg,
            'create_time': comment.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        # 回复评论数据添加
        reply_list = []
        reply_comments = BlogsComment.query.filter_by(comment_id=comment.id, status=1)
        for reply in reply_comments:
            reply_dict = {
                "msg": reply.msg,
                "nick_name": reply.nick_name,
                'create_time': reply.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            reply_list.append(reply_dict)
        comment_dict["reply_list"] = reply_list
        comment_list.append(comment_dict)
    # 3.返回
    return jsonify(
        comment_list=comment_list,
        page=page,
        result=1
    )


@blog_blueprint.route('/add/comment', methods=['POST'])
def add_comment():
    """添加评论"""
    # 1.获取blog_id
    blog_id = int(request.form.get('blog_id', '0'))
    msg = request.form.get('msg')
    if not all([blog_id, msg]):
        return jsonify(result=0)

    # 2.保存评论信息到数据库
    comment = BlogsComment()
    comment.msg = msg
    comment.blogs_id = blog_id
    try:
        db.session.add(comment)
        db.session.commit()
    except:
        current_app.logger_blog.error('保存评论信息访问数据库失败')
        return jsonify(result=-1)
    # 3.返回结果，提示需要审核之后才能显示
    return jsonify(result=1)


@blog_blueprint.route('/add/reply', methods=['POST'])
def add_reply():
    """添加回复"""
    # 1.获取comment_id
    blog_id = int(request.form.get('blog_id', '0'))
    comment_id = int(request.form.get('comment_id', '0'))
    msg = request.form.get('msg')
    if not all([comment_id, blog_id, msg]):
        return jsonify(result=0)

    # 2.保存评论信息到数据库
    comment = BlogsComment()
    comment.msg = msg
    comment.comment_id = comment_id
    comment.blogs_id = blog_id
    try:
        db.session.add(comment)
        db.session.commit()
    except:
        current_app.logger_blog.error('保存评论信息访问数据库失败')
        return jsonify(result=-1)
    # 3.返回结果，提示需要审核之后才能显示
    return jsonify(result=1)


@blog_blueprint.route('/message', methods=['GET'])
def show_message():
    """留言页展示"""
    return render_template(
        'blog/message.html',
        title='留言 | 卡拗口的博客',
    )


@blog_blueprint.route('/add/message', methods=['POST'])
def add_message():
    """留言页面提交"""
    # 提交留言数据，需要审核之后才能发布
    msg = request.form.get('msg')
    if not msg:
        return jsonify(result=0)
    message = BlogsMessage()
    message.msg = msg
    try:
        db.session.add(message)
        db.session.commit()
    except:
        current_app.logger_blog.error('保存留言信息访问数据库失败')
        return jsonify(result=-1)
    return jsonify(result=1)


@blog_blueprint.route('/get_message_list')
def get_message_list():
    """留言接口，vue请求留言数据"""
    # 1.查询留言的数据
    page = int(request.args.get('page', '1'))
    # 2.分页查询数据
    pagination = BlogsMessage.query.filter_by(isDelete=False, status=1). \
        order_by(BlogsMessage.id.asc()).paginate(page, 8, False)

    message_list = []
    # 3.转换为JSON数据
    for message in pagination.items:
        message_dict = {
            'avatar': message.avatar_url,
            'nick_name': message.nick_name,
            'msg': message.msg,
            'create_time': message.create_time.strftime("%Y-%m-%d")
        }
        message_list.append(message_dict)
    return jsonify(
        message_list_left=message_list[0::2],
        message_list_right=message_list[1::2],
        page=page,
    )


@blog_blueprint.route('/laboratory')
def laboratory():
    """实验室页面"""
    return render_template('blog/lab.html', title='实验室 | 卡拗口的博客')


@blog_blueprint.route('/links')
def links():
    """前端导航页"""
    return render_template('blog/links.html', title='前端导航 | 卡拗口的博客')


@blog_blueprint.route('/about')
def about():
    """关于我们"""
    return render_template('blog/about.html', title='关于 | 卡拗口的博客')


@blog_blueprint.route('/show')
def show():
    text = '# hell'


    # from markdown import markdown
    # text = markdown(text)
    # print()
    return render_template('admin/text.html', text=text)
