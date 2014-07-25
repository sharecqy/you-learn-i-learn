$(document).ready(function(){
	var cursor=0;
	function getCookie(name){
		var c=document.cookie.match("\\b"+name+"=([^;]*)\\b");
		return c?c[1]:undefined;
	};
	/*Guess button reaction*/
	$(".operation").click(function(){
                thistag=$(this);
                voted=$(this).parent().attr('voted');
                if(voted==1)return false;
                targetid=$(this).attr('id');
                cat=$(this).attr('cat');
                vote={};
                if(cat==1 || cat==3){}
                else vote['push']=1;
                if(cat==1 || cat==2){vote['tp']=targetid;url="topic/tpvote";}
                else {vote['com']=targetid;url="topic/comvote";}
                vote['_xsrf']=getCookie('_xsrf');
		        $.ajax({
                        url:url,
                        type:'post',
                        datatype:'text',
                        data:jQuery.param(vote),
                        success:function(data){
                                if(data=="ok"){
                                        thistag.parent().attr("voted","1");
                                        thistag.addClass("highlighted");
                                        vc=thistag.parent().children('.vote_count');
                                        count=parseInt(vc.text(),10);
                                        if(vote['push'])vc.text(count+1);
                                        else vc.text(count-1);
                                        }
                                else {
                                        thistag.parent().attr('voted',"1");
                                        thistag.addClass("highlighted");
                                        alert("You have voted!") ; 
                                }
                        },
                        error: function (data, textStatus, jqXHR) { 
                                alert("there are mistakes.") ; 
                        },
                });
	});
        
        $('#comment form').validate({
        rules:{
            comment:{
                required:true,
            },
        },
        messages: {  
            comment: {  
                required: "Comment shouldn't be empty!",  
            },  
        },  
        success:function(label){
            //label.text('Your input is ok');
        }
    });

});
