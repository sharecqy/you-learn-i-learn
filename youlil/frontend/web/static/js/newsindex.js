$(document).ready(function(){
	var cursor=0;
	function getCookie(name){
		var c=document.cookie.match("\\b"+name+"=([^;]*)\\b");
		return c?c[1]:undefined;
	};
	/*Guess button reaction*/
	$("#guess_btn").click(function(){
		cursor+=1;
		$.ajax({
                url:'/myindex',
                type:'post',
                datatype:'json',
                data:jQuery.param({'cursor':cursor,'_xsrf':getCookie('_xsrf')}),
                success:function(data){
                        var url=data['redirect'];
                	var arts=data['rec'];
                        if(url)
                        {
                            location.href =url;
                        }
                        else
                        {
                                $('#arts .art').each(function(i){
                                $(this).find('.art_title').html("<a href='/news?art="+arts[i].art_id+"'><strong class='title'>"+arts[i].title+"</strong></a>");
                                $(this).find('.art_info').html("<span >Category:"+arts[i].cat_name+"</span>")//<span>&nbsp&nbspHardness:"+arts[i].hardness+"</span>");
                                $(this).find('.art_desc').html(arts[i].description);
                                });
                        }

                },
                error: function (data, textStatus, jqXHR) { 
                	alert(data.responseText);
                },
        });
	});

});
