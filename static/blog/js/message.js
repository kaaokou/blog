var cur_page = 0; // 当前页
var is_can_get = true;  // 定义一个bool在滚动的时候判定
var is_bottom = false;


$(function () {
    //初始化vue对象
    vue_message_con = new Vue({
        el: '#message_list_con',
        delimiters: ['[[', ']]'],  //将语法中的{{换成[[，将}}换成]]
        data: {
            message_list_left: [],
            message_list_right: [],
            left_lenght:0,
            right_lenght:0,
        }
    });

        // TODO 留言提交
    $(".comment_form").submit(function (e) {
        // 阻止默认提交
        e.preventDefault();
        var msg = $("#msg").val();
        if (!msg) {
            alert("请输入留言内容！");
            return;
        }
        $.post("/add/message", {
            "csrf_token": $("#csrf_token").val(),
            "msg": msg
        }, function (data) {
            if (data.result == 1) {
                // 提交成功，刷新评论显示
                $("#msg").val("");
                // 更新评论数
                $('.comments-form__success').show().delay(1000).hide(0);
            }
        })

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
            get_message_list();
        }
    });

    // 初始化获取数据
    get_message_list();

});

// TODO 获取评论数据
function get_message_list() {
    // 由于js代码是异步的，为了防止重复发情请求，所以这里置为false
    is_can_get = false;
    // 获取评论数据
    $.get("/get_message_list", {
        "page": cur_page + 1
    }, function (data) {
        if (cur_page == 0) {
            //请求第一页，说明刚进入一个新的分类，则进行赋值
            vue_message_con.message_list_left = data.message_list_left;
            vue_message_con.message_list_right = data.message_list_right;
        }
        else {
            //请求页不是第一页，说明在当前分类的基础上进行了向下滚动，则进行拼接
            vue_message_con.message_list_left = vue_message_con.message_list_left.concat(data.message_list_left);
            vue_message_con.message_list_right = vue_message_con.message_list_right.concat(data.message_list_right);
        }
        vue_message_con.left_lenght =  vue_message_con.message_list_left.length;
        vue_message_con.right_lenght =  vue_message_con.message_list_right.length;
        // 页面置为当前请求的页面
        cur_page = data.page;
        // 将can_get改为true
        is_can_get = true;
        // 判断是否到底
        if (data.message_list_right.length < 4) {
            is_bottom = true;
        }

    })

}


