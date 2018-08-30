$(function () {
     //初始化vue对象
    vue_list_con = new Vue({
        el: '.list_con',
        delimiters: ['[[', ']]'],//将语法中的{{换成[[，将}}换成]]
        data: {
            news_list: []
        }
    });
    // 加载页面的时候调用一次
    updateNewsData();


    // 首页分类切换
    $('.menu li').click(function () {
        var clickCid = $(this).attr('data-cid');
        $('.menu li').each(function () {
            $(this).removeClass('active')
        });
        $(this).addClass('active');

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
            updateNewsData();
        }
    })
});