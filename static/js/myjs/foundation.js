$(function(){
	(function(){
        $('input[name="file"]').fileupload({
            url: '/upload/basicprocess',
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
                $.get("/files/basicprocess",function(data){
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

        $( "#contrast" ).slider({
            orientation: "horizontal",
            range:"min",
            min:0,
            max: 100,
            value:10,
            stop: refreshcontrast
            //change: refreshSwatch
        });
        $( "#hue" ).slider({
            orientation: "horizontal",
            range:"min",
            min:0,
            max: 20,
            value:10,
            stop: refreshhue
            //change: refreshSwatch
        });
        $( "#value" ).slider({
            orientation: "horizontal",
            range:"min",
            min:0,
            max: 20,
            value:10,
            stop: refreshvalue
            //change: refreshSwatch
        });
        $( "#saturation" ).slider({
            orientation: "horizontal",
            range:"min",
            min:0,
            max: 20,
            value:10,
            stop: refreshsaturation
            //change: refreshSwatch
        });

        $("#tools_save").click(function () {
            $.post("/save/basicprocess",function (data) {
                if(data.code==200){
                    alert("保存成功！");
                }
                else{
                    alert("保存失败！");
                }
            })
        });
   })();

	function refreshcontrast() {
	    $( "#saturation" ).slider("value",10);
	    $( "#hue" ).slider("value",10);
	    $( "#value" ).slider("value",10);
	    $( "#amount_saturation" ).val(1);
	    $(" #amount_hue" ).val(1);
	    $( "#amount_value" ).val(1);
	    var contrast=$( "#contrast" ).slider( "value" )/10;
	    $( "#amount_contrast" ).val(contrast );
	    $.post("/basicprocess/contrast", {"contrast": contrast}, function(data){
	        if(data.code==404){
                alert("请先加载图片！");
            }
            else {
                putImg('resImg', data.img64);
            }

	    });
	}
	function refreshvalue() {
        $( "#saturation" ).slider("value",10);
        $( "#hue" ).slider("value",10);
        $( "#contrast" ).slider("value",10);
        $( "#amount_saturation" ).val(1);
        $(" #amount_hue" ).val(1);
        $( "#amount_contrast").val(1);

        var value=$( "#value" ).slider( "value" )/10;
        $( "#amount_value" ).val(value );
        $.post("/basicprocess/value", {"value": value}, function(data){
            if(data.code==404){
                alert("请先加载图片！");
            }
            else {
                putImg('resImg', data.img64);
            }
        });
    }
    function refreshsaturation() {
        $( "#contrast" ).slider("value",10);
        $( "#hue" ).slider("value",10);
        $( "#value" ).slider("value",10);
        $( "#amount_contrast" ).val(1);
        $(" #amount_hue" ).val(1);
        $( "#amount_value" ).val(1);

        var saturation=$( "#saturation" ).slider( "value" )/10;
        $( "#amount_saturation" ).val(saturation );
        $.post("/basicprocess/saturation", {"saturation": saturation}, function(data){
            if(data.code==404){
                alert("请先加载图片！");
            }
            else {
                putImg('resImg', data.img64);
            }
        });
    }
    function refreshhue() {
        $( "#saturation" ).slider("value",10);
        $( "#contrast" ).slider("value",10);
        $( "#value" ).slider("value",10);
        $( "#amount_saturation" ).val(1);
        $(" #amount_contrast" ).val(1);
        $( "#amount_value" ).val(1);

        var hue=$( "#hue" ).slider( "value" )/10;
        $( "#amount_hue" ).val(hue );
        $.post("/basicprocess/hue", {"hue": hue}, function(data){
            if(data.code==404){
                alert("请先加载图片！");
            }
            else {
                putImg('resImg', data.img64);
            }
        });
    }
    function putResRawImgs(base){ // 将[resImg,rawImg]显示出来
        putImg('rawImg',base);
        putImg('resImg',base);
    }
    function putImg (id, base){  //将base64 img 放到#id中
        var img = '<img width=400px height=400px src="data:image/png;base64,'+base+'" class="inline"/> ';
        $('#'+id).html(img);
    }
});