$(document).ready(function(){
  /*form validation*/
    $('#edittopic').validate({
        rules:{
            title:{
                required:true,
                maxlength:40,
            },
            content:{
                required:true,
            },
            tags:{
                required:true,
            },
        },
        messages: {  
            title: {  
                required: "Title is required.",  
                maxlength:"Title's max lenghth is 40",
            },  
            content:{ 
                required:"Content can't be empty.",
            },  
            tags:{
                required:"Tags are requeired,splitted with blank space",
            },
        },  
        success:function(label){
            //label.text('Your input is ok');
        }
    });
});
