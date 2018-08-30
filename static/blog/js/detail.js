var cur_page = 0; // 当前页
var is_can_get = true;  // 定义一个bool在滚动的时候判定
var is_bottom = false;
var reply = '回复';

$(function () {
    //初始化vue对象
    vue_comment_con = new Vue({
        el: '#comments_items',
        delimiters: ['[[', ']]'],  //将语法中的{{换成[[，将}}换成]]
        data: {
            comment_list: []
        }
    });
    // 初始化获取数据
    get_comment_list();

    // TODO 评论提交
    $("#comment_submit").click(function () {
        // 阻止默认提交
        // e.preventDefault();
        var msg = $("#msg").val();
        if (!msg) {
            alert("请输入评论内容！");
            return;
        }
        var _this = $(this);
        $.post("/add/comment", {
            "csrf_token": $("#csrf_token").val(),
            "msg": msg,
            'blog_id': $('#blog_id').val()
        }, function (data) {
            if (data.result == 1) {
                // 提交成功，刷新评论显示
                $("#msg").val("");
                // 更新评论数

                _this.parent().parent().prev().children('.comments-form__success').show().delay(1000).hide(0);
                // $('.comments-form__success').show().delay(1000).hide(0);
            }
        })

    });


    // TODO 点击评论显示输入框
    $('#comments_items').delegate('.comments-form__btn', 'click', function () {
        // 获取blog_id,comment_id,msg
        var msg = $(this).parent().parent().prev().children('.msg').val();

        if(!msg){
            alert('请输入回复内容！');
            return
        }
        // 发送请求
        var _this = $(this);
        $.post("/add/reply", {
            "csrf_token": $("#csrf_token").val(),
            "msg": msg,
            'blog_id': $('#blog_id').val(),
            'comment_id': $(this).attr("comment_id")
        }, function (data) {
            if (data.result == 1) {
                // 提交成功，刷新评论显示
                _this.parent().parent().prev().children('.msg').val('');
                // 更新评论数
                _this.parent().parent().prev().children('.comments-form__success').show().delay(1000).hide(0);
            }
        })

    });

    // TODO 显示回复输入框
    $('#comments_items').delegate('.comment-item__reply-btn', 'click', function () {
        if (reply == '回复') {
            reply = '取消回复'
        }
        else {
            reply = '回复'
        }
        $(this).html(reply);
        $(this).parent().parent().children(':last-child').toggle();

    });
    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100 && is_can_get && !is_bottom) {
            // TODO 判断页数，去更新新闻数据
            get_comment_list();
        }
    });


});

// TODO 获取评论数据
function get_comment_list() {
    // 由于js代码是异步的，为了防止重复发情请求，所以这里置为false
    is_can_get = false;
    // 获取评论数据
    $.get("/get_comment_list/" + $('#blog_id').val(), {
        "page": cur_page + 1
    }, function (data) {

        if (data.result == 1) {
            if (cur_page == 0) {
                //请求第一页，说明刚进入一个新的分类，则进行赋值
                vue_comment_con.comment_list = data.comment_list;
            }
            else {
                //请求页不是第一页，说明在当前分类的基础上进行了向下滚动，则进行拼接
                vue_comment_con.comment_list = vue_comment_con.comment_list.concat(data.comment_list);
            }

            // 页面置为当前请求的页面
            cur_page = data.page;
            // 将can_get改为true
            is_can_get = true;
            // 判断是否到底
            if (data.comment_list.length < 4) {
                is_bottom = true;
            }
        }

    })

}


