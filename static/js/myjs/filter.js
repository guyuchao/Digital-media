$(function(){
	(function(){
	    $('#Mean-filtering').click(function () {
            $.post("/filtering/mean-filter", function(data){
                if(data.code==404){
                    alert("请先加载图片！");
                }
                else {
                    putImg('resImg', data.img64);
                }
            })
        });
        $('#Median-filtering').click(function () {
            $.post("/filtering/median-filter", function(data){
                if(data.code==404){
                    alert("请先加载图片！");
                }
                else {
                    putImg('resImg', data.img64);
                }
            })
        });
        $('#Gaussian-filtering').click(function () {
            $.post("/filtering/gaussian-filter", function(data){
                if(data.code==404){
                    alert("请先加载图片！");
                }
                else {
                    putImg('resImg', data.img64);
                }
            })
        });
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
        $('#Bilateral-filtering').click(function () {
            $.post("/filtering/bilateral-filter", function(data){
                if(data.code==404){
                    alert("请先加载图片！");
                }
                else {
                    putImg('resImg', data.img64);
                }
            })
        });
        $('#Salt-noise').click(function () {
            $.post("/noise/salt_noise", function(data){
                if(data.code==404){
                    alert("请先加载图片！");
                }
                else {
                    putResRawImgs(data.img64);
                }
            })
        });
        $('#Gaussian-noise').click(function () {
            $.post("/noise/gaussian_noise", function(data){
                if(data.code==404){
                    alert("请先加载图片！");
                }
                else {
                    putResRawImgs(data.img64);
                }
            })
        });

        $('#no-wave-filtering').click(function () {
            $.post("/clear", function(data){
                if(data.code==404){
                    alert("请先加载图片！");
                }
                else {
                    putImg('resImg', data.img64);
                }
            })
        });

        $("#tools_save").click(function () {
            $.post("/save/filter",function (data) {
                if(data.code==200){
                    alert("保存成功！");
                }
                else{
                    alert("保存失败！");
                }
            })
        });
        $('input[name="file"]').fileupload({
            url: '/upload/filter',
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
                $.get("/files/filter",function(data){
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