function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function(){
    // $(".news_edit").submit(function (e) {
    //     e.preventDefault();
    // });


    // TODO 加载图片自动显示
     $(".input_file").change(function () {
        // 读取文件
        var current_pic = this.files[0];
        // 预览图片处理
        preview_picture(current_pic);
    });

    function preview_picture(pic) {
        // 创建文件读取对象
        var file_reader = new FileReader();
        // 读取
        file_reader.readAsDataURL(pic);
        // 加载完成之后 --> 显示
        file_reader.onload = function (e) {
            $("#image").attr("src", this.result).show();
        }
    }
});

// 点击取消，返回上一页
function cancel() {
    history.go(-1)
}