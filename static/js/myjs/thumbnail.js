$(function(){
	$.get("/thumbnail",function(data){
	    var line=data.len/3
        var remain=data.len%3

        for(var i=0;i<line;i++) {
	        var src1='img'+(i*3+0);
	        var src2='img'+(i*3+1);
	        var src3='img'+(i*3+2);
            var html = '<div class="container">' +
                '<div class="row">' +
                '<div class="col-md-4 col-xs-4">' +
                '<a href="#imageModal7" class="portfolio-link" data-toggle="modal">' +
                '<img src="'+data[src1]+'" class="img-responsive" alt="">' +
                '</a>' +
                '</div>' +
                '<div class="col-md-4 col-xs-4">' +
                '<a href="#imageModal8" class="portfolio-link" data-toggle="modal">' +
                '<img src="'+data[src2]+'" class="img-responsive" alt="">' +
                '</a>' +
                '</div>' +
                '<div class="col-md-4 col-xs-4">' +
                '<a href="#imageModal9" class="portfolio-link" data-toggle="modal">' +
                '<img src="'+data[src3]+'" class="img-responsive" alt="">' +
                '</a>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<hr>';
            $('#page-wrapper').append(html);
        }
        var html = '<div class="container">' +
                '<div class="row">' ;
        for(var i=0;i<remain;i++){
	        var src='img'+(3*line+i);
	        html+=
                '<div class="col-md-4 col-xs-4">' +
                '<a href="#imageModal7" class="portfolio-link" data-toggle="modal">' +
                '<img src="'+data[src]+'" class="img-responsive" alt="">' +
                '</a>' +
                '</div>';


        }
        html+='</div>' +
                '</div>' +
                '<hr>';
        $('#page-wrapper').append(html);

	});
});