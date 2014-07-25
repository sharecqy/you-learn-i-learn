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
                url:'/videoindex',
                type:'post',
                datatype:'json',
                data:jQuery.param({'cursor':cursor,'_xsrf':getCookie('_xsrf')}),
                success:function(data){
                        var url=data['redirect'];
                        var videos=data['rec'];
                        
                        if(url)
                        {
                            location.href =url;
                        }
                        else
                        {
                             // var movies=$.parseJSON(data)['rec'];
                            $('#videos .video_block').each(function(i){
                                    $(this).find('.video_picture').html("<a href='"+videos[i].link+"'"+" target='_blank'><img class='img-rounded video_img' src='"+videos[i]['thumbnail']+"'/></a>");
                                    $(this).find('.video_info').find('.video_title').html("<a href='"+videos[i].link+"' target='_blank'><strong class='title'>"+videos[i].title+"</strong></a>");
                                    $(this).find('.video_info').find('.video_viewcount').html("<span>Viewd:"+videos[i].view_count+"</span>");
                                    var tags=videos[i].tags;
                                    $(this).find('.video_info').find('.video_tags').empty();
                                    for (x in tags)
                                    {
                                            $(this).find('.video_info').find('.video_tags').append('<span class="label">'+tags[x]+'</span>').append('<span class="">'+' '+'</span>');
                                    }
                            });                           
                        }

                },
                error: function (data, textStatus, jqXHR) { 
                        alert(data.responseText);
                },
        });
        });


});