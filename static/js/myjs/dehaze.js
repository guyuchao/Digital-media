$(function(){
	(function(){

        $('#Dehaze').click(function () {
            $.post("/dehaze", function(data){
                if(data.code==404){
                    alert("请先加载图片！");
                }
                else {
                    putImg('resImg', data.img64);
                }
            })
        });


        $("#tools_save").click(function () {
            $.post("/save/dehaze",function (data) {
                if(data.code==200){
                    alert("保存成功！");
                }
                else{
                    alert("保存失败！");
                }
            })
        });
        $('input[name="file"]').fileupload({
            url: '/upload/dehaze',
            Type: "POST",
            autoUpload: true,
            acceptFileTypes:/\.(jpg|jpeg)$/i,// 文件格式
            maxFileSize: 99 * 1024 * 1024, //文件大小
            dataType:"json",
            // 设置验证失败的提示信息
            messages: {
                maxFileSize: 'File exceeds maximum allowed size of 99MB',
                acceptFileTypes: 'File type not allowed'
            },
            done: function(e,data) {
                $.get("/files/dehaze",function(data){
                    //alert(data.img64);
                    putResRawImgs(data.img64);
                });
                //alert("success");
                // 上传成功的回调函数，可以弹出“上传成功”之类的弹框
            },
            fail: function() {
                alert("s");
                 // 上传失败的回调函数，可以弹出“上传失败”之类的弹框
            }
        });

   })();


    function putResRawImgs(base){ // 将[resImg,rawImg]显示出来
        putImg('rawImg',base);
        putImg('resImg',base);
    }
    function putImg (id, base){  //将base64 img 放到#id中
        var img = '<img width=400px height=400px src="data:image/png;base64,'+base+'" class="inline"/> ';
        $('#'+id).html(img);
    }
});