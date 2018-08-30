var currentCid = 0; // 当前分类 id
var cur_page = 0; // 当前页
var is_can_get = true;  // 定义一个bool在滚动的时候判定
var is_bottom = false;


$(function () {
    //初始化vue对象
    vue_bloglist_con = new Vue({
        el: '.posts_items_con',
        delimiters: ['[[', ']]'],  //将语法中的{{换成[[，将}}换成]]
        data: {
            blog_list: []
        }
    });

    // 初始化获取数据
    get_blog_list();


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
            if (currentCid == -1){
                search_detail_list();
            }
            else{
                get_blog_list();
            }

        }
    });


    // TODO blog分类切换
    $('.post_menu li').click(function () {
        var clickCid = $(this).attr('data-id');
        var index = $(this).index();
        // $('.post_menu li').each(function () {
        //     $(this).removeClass('active')
        // });
        // $(this).addClass('active');
        $('.post-category__slider').css({'top': index * 40 + "px"});

        if (clickCid != currentCid) {
            // TODO 去加载新闻数据
            // 更新分类和初始化请求页面
            currentCid = clickCid;
            cur_page = 0;
            is_bottom = false;
            get_blog_list();
        }

    });

    // TODO 搜索栏
    $('#search').click(function () {
        // alert('天机');
        // 初始化数据
        currentCid = -1;
        cur_page = 0;
        is_bottom = false;
        search_detail_list();
    });


});

// TODO 获取评论数据
function get_blog_list() {
    // 由于js代码是异步的，为了防止重复发情请求，所以这里置为false
    is_can_get = false;
    // 获取评论数据
    $.get("/get_detail_list", {
        "page": cur_page + 1,
        "category_id": currentCid
    }, function (data) {
        if (cur_page == 0) {
            //请求第一页，说明刚进入一个新的分类，则进行赋值
            vue_bloglist_con.blog_list = data.blog_list;

        }
        else {
            //请求页不是第一页，说明在当前分类的基础上进行了向下滚动，则进行拼接
            vue_bloglist_con.blog_list = vue_bloglist_con.blog_list.concat(data.blog_list);

        }
        // 页面置为当前请求的页面
        cur_page = data.page;
        // 将can_get改为true
        is_can_get = true;
        // 判断是否到底
        if (data.blog_list.length < 4) {
            is_bottom = true;
        }

    })

}

// TODO 搜索blog
function search_detail_list() {
    // 由于js代码是异步的，为了防止重复发情请求，所以这里置为false
    is_can_get = false;
    // 获取评论数据
    $.get("/search_detail_list" + '?search_name=' + $('#search_name').val(), {
        "page": cur_page + 1
    }, function (data) {
        // 如果返回的数据为空
        if(data.blog_list.length == 0){
            $('.post-search__result').show().delay(1000).hide(0);
            return;
        }

        // 将状态栏置于全部博文
        $('.post-category__slider').css({'top': "0px"});
        if (cur_page == 0) {
            //请求第一页，说明刚进入一个新的分类，则进行赋值
            vue_bloglist_con.blog_list = data.blog_list;

        }
        else {
            //请求页不是第一页，说明在当前分类的基础上进行了向下滚动，则进行拼接
            vue_bloglist_con.blog_list = vue_bloglist_con.blog_list.concat(data.blog_list);

        }
        // 页面置为当前请求的页面
        cur_page = data.page;
        // 将can_get改为true
        is_can_get = true;
        // 判断是否到底
        if (data.blog_list.length < 4) {
            is_bottom = true;
        }
    })

}