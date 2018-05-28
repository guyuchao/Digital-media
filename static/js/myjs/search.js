
$(function(){
	(function(){
	    $('#begin_search').click(function () {
			$.get("/searchimg",function(data){
				if(data.code==404){
					alert("请先上传图片！");
				}
				else {
                    var big = '<ul>' +
                        '<li style="z-index: 1"><img width=750px height=450px src="data:image/png;base64,' + data.img0 + '"></li>' +
                        '<li><img width=750px height=450px src="data:image/png;base64,' + data.img1 + '"></li>' +
                        '<li><img width=750px height=450px src="data:image/png;base64,' + data.img2 + '"></li>' +
                        '<li><img width=750px height=450px src="data:image/png;base64,' + data.img3 + '"></li>' +
                        '<li><img width=750px height=450px src="data:image/png;base64,' + data.img4 + '"></li>' +
                        '<li><img width=750px height=450px src="data:image/png;base64,' + data.img5 + '"></li>' +
                        '<li><img width=750px height=450px src="data:image/png;base64,' + data.img6 + '"></li>' +


                        '</ul>';
                    /*var big='<ul>' +
                        '           <li style="z-index: 1"><img width=500px height=300px src="../static/2.jpg"></li>' +
                        '            <li><img width=500px height=300px src="../static/2.jpg"></li>' +
                        '            <li><img width=500px height=300px src="../static/2.jpg"></li>' +
                        '        </ul>';*/
                    $('#big_pic').append(big);
                    var small = '<ul>' +
                        '<li id="img0" style="filter: alpha(opacity:100); opacity: 1;"><img src="data:image/png;base64,' + data.img0 + '"></li>' +
                        '<li><img src="data:image/png;base64,' + data.img1 + '"></li>' +
                        '<li><img src="data:image/png;base64,' + data.img2 + '"></li>' +
                        '<li><img src="data:image/png;base64,' + data.img3 + '"></li>' +
                        '<li><img src="data:image/png;base64,' + data.img4 + '"></li>' +
                        '<li><img src="data:image/png;base64,' + data.img5 + '"></li>' +
                        '<li><img src="data:image/png;base64,' + data.img6 + '"></li>' +

                        '</ul>';
                    $('#small_pic').html(small);
                }
			});
		});
		$('input[name="file"]').fileupload({
			url: '/upload/search',
			Type: "POST",
			autoUpload: true,
			acceptFileTypes:/\.(jpg|jpeg)$/i,// 文件格式
			maxFileSize: 99 * 1024 * 1024, //文件大小
			dataType:"json",
			messages: {
				maxFileSize: 'File exceeds maximum allowed size of 99MB',
				acceptFileTypes: 'File type not allowed'
			},
			done: function(e,data) {
				alert("上传成功");
				//alert("data");
				/*$.get("/simimg/"+data.result.filename,function(data,status,header){
					//var content = decodeUtf8(data);
					//alert(typeof content)
				   // data=new Buffer(JSON.stringify({"hello":"world"})).toString("base64");
					 var enc = $('#decode');
					 $.base64.utf8encode = true;
					 enc.val($.base64.atob(data, true));
					alert(data['img0']);
					putResRawImgs(data['img0']);

				});*/
			},
			fail: function() {
				alert("s");
			}
		});

		var oDiv = document.getElementById('div1');
		var oBtnPrev = getByClass(oDiv, 'prev')[0];
		var oBtnNext = getByClass(oDiv, 'next')[0];

		oBtnOnMouse();
		oBtnOnClick();

		//点击小图大图拉下切换效果  层级z-index
		var oDivSmall = getByClass(oDiv,'small_pic')[0];
		var aLiSmall = oDivSmall.getElementsByTagName('li');
		var oDivBig = getByClass(oDiv,'big_pic')[0];
		var aLiBig = oDivBig.getElementsByTagName('li');

		function getByClass(oParent, sClass) {

            var aEle = oParent.getElementsByTagName('*');
            var aResult = [];

            for(var i = 0; i < aEle.length; i++) {
                if (aEle[i].className == sClass) {
                    aResult.push(aEle[i]);
                }
            }
            return aResult;
        }
		//初始化一个变量控制图层显示优先级
		var nowZIndex = 1;
		var now = 0;
		for(var i = 0; i < aLiSmall.length; i++) {
			aLiSmall[i].index = i;
			aLiSmall[i].onclick = function () {
				//如果显示的是当前这张,返回flase 这个函数终止
				if(this.index == now) return;
				//如果显示不是当前这张,那么使得当前小图等于当前大图
				now = this.index;
				tab();
			};
			aLiSmall[i].onmouseover = function () {
				starMove(this, 'opacity', 100);
			};
			aLiSmall[i].onmouseout = function () {
				//如果显示的是当前这张,返回flase 这个函数终止
				if(this.index == now) return;
				starMove(this, 'opacity', 50);
			};
		}

		//oBtnOnMouse---左右按钮显示效果部分
		function oBtnOnMouse() {
			var oMarkLeft = getByClass(oDiv, 'mark_left')[0];
			var oMarkRight = getByClass(oDiv, 'mark_right')[0];
			oBtnPrev.onmouseover = oMarkLeft.onmouseover = function () {
				starMove(oBtnPrev, 'opacity', 100)
			};
			oBtnPrev.onmouseout = oMarkLeft.onmouseout = function () {
				starMove(oBtnPrev, 'opacity', 0)
			};
			oBtnNext.onmouseover = oMarkRight.onmouseover = function () {
				starMove(oBtnNext, 'opacity', 100)
			};
			oBtnNext.onmouseout = oMarkRight.onmouseout = function () {
				starMove(oBtnNext, 'opacity', 0)
			};
		}

		//封装--当前小图关联大图运动函数
		function tab() {
			var oUlSmall = oDivSmall.getElementsByTagName('ul')[0];
			aLiBig[now].style.zIndex = nowZIndex++;
			for(var i = 0; i < aLiSmall.length; i++) {
				starMove(aLiSmall[i], 'opacity', 60);
			}
			starMove(aLiSmall[now], 'opacity', 100);
			aLiBig[now].style.height = 0;
			starMove(aLiBig[now], 'height', 450);

			if(now == 0) {
				starMove(oUlSmall, 'left', 0);
			}
			else if(now == aLiSmall.length-2) {
				starMove(oUlSmall, 'left', -(now-2)*aLiSmall[0].offsetWidth)
			}
			else if(now == aLiSmall.length-1) {
				starMove(oUlSmall, 'left', -(now-3)*aLiSmall[0].offsetWidth)
			}
			else {
				starMove(oUlSmall, 'left', -(now-1)*aLiSmall[0].offsetWidth)
			}
		}

		//点击导航大图切换
		function oBtnOnClick() {
			oBtnPrev.onclick = function () {
				now--;
				if(now == -1) {
					now = aLiSmall.length-1;
				}
				tab();
			};
			oBtnNext.onclick = function () {
				now++;
				if(now == aLiSmall.length) {
					now = 0;
				}
				tab();
			};
		}

		// 自动播放 即自动点击oBtnPrev.onclick加入定时器循环.
		var timer = setInterval(oBtnPrev.onclick, 3000);
		oDiv.onmouseover = function () {
			clearInterval(timer)
		};
		oDiv.onmouseout = function () {
				timer = setInterval(oBtnPrev.onclick, 3000)
			};
	})();
	function getStyle(obj, name) {
		if(obj.currentStyle) {
			return obj.currentStyle
		}
		else {
			return getComputedStyle(obj, false) [name];
		}
	}

	function starMove(obj, attr, iTarget) {
		clearInterval(obj.timer);
		obj.timer = setInterval(move,30);
		function move() {
			var current = null;
			//如果传进来的样式是透明度
			if(attr == 'opacity') {
				//用浮点 并且乘以一百变成整数  0.3*100 ==30
				//Math.round 四舍五入
				current = Math.round(parseFloat(getStyle(obj,attr))*100);
			} else { //其他样式 例如宽高 等数字是整数的
				current = parseInt(getStyle(obj,attr));
			}

			var speed = (iTarget-current) / 10;
			speed = speed > 0 ? Math.ceil(speed) : Math.floor(speed);

			if(current == iTarget){
				clearInterval(obj.timer);
			} else {
				if(attr == 'opacity') {
					obj.style.filter = 'alpha(opacity:'+current + speed+')';
					obj.style.opacity = (current + speed)/100;

				} else {
					obj.style[attr] = current + speed + 'px';
				}
			}
		}
	}
});