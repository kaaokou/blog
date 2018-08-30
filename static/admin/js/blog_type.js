function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {
    var $a = $('.edit');
    var $del = $('.delete');  // 增加的删除按钮
    var $add = $('.addtype');
    var $pop = $('.pop_con');
    var $cancel = $('.cancel');
    var $confirm = $('.confirm');
    var $error = $('.error_tip');
    var $input = $('.input_txt3');
    var sHandler = 'edit';
    var sId = 0;  // 获取的id值


    $a.click(function () {
        sHandler = 'edit';
        sId = $(this).parent().siblings().eq(0).html();
        $pop.find('h3').html('修改分类');
        $pop.find('.input_txt3').val($(this).parent().prev().html());
        $pop.show();
    });
    $del.click(function () {
        // 删除按钮响应点击
        sHandler = 'delete';
        sId = $(this).parent().siblings().eq(0).html();
        $pop.find('h3').html('删除分类');
        $pop.find('.input_txt3').val("你确定要删除【" + $(this).parent().prev().prev().html() + "】分类吗");
        $pop.show();
    });

    $add.click(function () {
        sHandler = 'add';
        $pop.find('h3').html('新增分类');
        $input.val('');
        $pop.show();
    });

    $cancel.click(function () {
        $pop.hide();
        $error.hide();
    });

    $input.click(function () {
        $error.hide();
    });

    $confirm.click(function () {
        // TODO 修改
        if (sHandler == 'edit') {
            var sVal = $input.val();
            if (sVal == '') {
                $error.html('输入框不能为空').show();
                return;
            }
            $.post("/admin/blog_type", {
                "csrf_token": $("#csrf_token").val(),
                "name": sVal,
                "id": sId,
                "action": 2
            }, function (data) {
                if (data.result == 1) {
                    // 重新加载
                    location.reload();
                }
                else if (data.result == 0) {
                    $error.html("输入内容不能为空");
                    $error.show();
                }
                else if (data.result == -2) {
                    // 已存在分类
                    $error.html("分类已存在");
                    $error.show();
                }
            })
        }
        // TODO 新增分类
        else if(sHandler == 'add'){
            var sVal = $input.val();
            if (sVal == '') {
                $error.html('输入框不能为空').show();
                return;
            }
            // 发送ajax请求
            $.post("/admin/blog_type", {
                "csrf_token": $("#csrf_token").val(),
                "name": sVal,
                "id": -1,
                "action": 1
            }, function (data) {
                if (data.result == 1) {
                    // 重新加载
                    location.reload();
                }
                else if (data.result == 0) {
                    $error.html("输入内容不能为空");
                    $error.show();
                }
                else if (data.result == -2) {
                    // 已存在分类
                    $error.html("分类已存在");
                    $error.show();
                }
            })
        }
         // TODO 新增分类
        else if(sHandler == 'delete'){

            // 发送ajax请求
            $.post("/admin/blog_type_del", {
                "csrf_token": $("#csrf_token").val(),
                "id": sId
            }, function (data) {
                if (data.result == 1) {
                    // 重新加载
                    location.reload();
                }
            })
        }

    })
});

function add_type(action) {
// 发送ajax请求


}