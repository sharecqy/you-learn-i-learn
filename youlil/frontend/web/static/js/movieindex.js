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
                url:'/movieindex',
                type:'post',
                datatype:'json',
                data:jQuery.param({'cursor':cursor,'_xsrf':getCookie('_xsrf')}),
                success:function(data){
                        var url=data['redirect'];
                        var movies=data['rec'];
                        if(url)
                        {
                            location.href =url;
                        }
                        else
                        {
                            // var movies=$.parseJSON(data)['rec'];
                            $('#movies .movie_block').each(function(i){
                                    $(this).find('.movie_picture').html("<a href='/movie?mid="+movies[i].id+"'><img class='img-rounded movie_img' src='"+movies[i]['posters']['original']+"'/><span><strong><em>IMDB:"+movies[i].ratings.audience_score+"</em></strong></span></a>");
                                    $(this).find('.movie_info').find('.movie_title').html("<a href='/movie?mid="+movies[i].id+"'><strong class='title'>"+movies[i].title+"</strong></a>");
                                    $(this).find('.movie_info').find('.movie_synposis').html("<span>Synopsis:"+movies[i].synposis+"</span>");
                                    var genres=movies[i].genres;
                                    $(this).find('.movie_info').find('.movie_genres').empty();
                                    for (x in genres)
                                    {
                                            $(this).find('.movie_info').find('.movie_genres').append('<span class="label">'+genres[x]+'</span>').append('<span class="">'+' '+'</span>');
                                    }
                            });
                        }

                },
                error: function (data, textStatus, jqXHR) { 
                        alert(data.responseText);
                },
        });
        });
        /*Tabs*/
         $('#tabs a').click(function (e) {
           e.preventDefault();
           $(this).tab('show');
         })

});

