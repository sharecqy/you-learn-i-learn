$(document).ready(function(){
	$("#switch_signup").click(function() {
		$('#login_area').attr('class','invisible');
		$('#signup_area').attr('class','visible');
	});
    $("#switch_signup").hover(function(){
        $("#switch_signup").css('color','#33CC99');
        },function(){
        $("#switch_signup").css('color','#999');
    });
	$("#switch_login").click(function() {
		$('#login_area').attr('class','visible');
		$('#signup_area').attr('class','invisible');
	});
    $("#switch_login").hover(function(){
        $("#switch_login").css('color','#33CC99')
        },function(){
        $("#switch_login").css('color','#999')
    });

     $('#youlil_login form').submit(function(e){
        $.ajax({
                url:'/login',
                type:'post',
                datatype:'json',
                data:$('#youlil_login form').serialize(),
                success:function(data){
                    window.location="/myindex";
                },
                error: function (data, textStatus, jqXHR) { 
                    $('#login_help').text(data.responseText); 
                },
        });
        e.preventDefault();
     });

    /*form validation*/
    $('#youlil_login form').validate({
        rules:{
            login_email:{
                required:true,
                email:true
            },
            login_password:{
                required:true,
                minlength:6,
            },
        },
        messages: {  
            login_email: {  
                required: "Email can't be empty",  
                email: "Email format isn't right"  
            },  
            login_password:{ 
                required:"Password can't be empty",
                minlength:"Password at least 6 letters",
            },  
        },  
        success:function(label){
            label.text('Your input is ok');
        }
    });

    $('#youlil_signup form').validate({
        rules:{
            signup_email:{
                required:true,
                email:true
            },
            signup_name:{
                required:true,
            },
            signup_password:{
                minlength:6,
                required:true
            },
            signup_passconf:{
                required:true,
                equalTo:'#signup_password',
            }

        },
        messages: {  
            signup_email: {  
                required: "Email can't be empty",  
                email: "Email format isn't right"  
            },  
            signup_name: {  
                required: "Nickname can't be empty",  
            },  
            signup_password:{ 
                required:"Password can't be empty",
                minlength:"Input 6 letters at least",
            },  
            signup_passconf:{
                required:"Input password again",
                equalTo:"Password doesn't equal",
            }
        },  
        success:function(label){
            label.text('Your input is ok');
        }
    });
});
