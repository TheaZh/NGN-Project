/**
 * Created by QW_Z on 11/7/17.
 */


$( document ).ready(function() {
    $("#login-button").click(function(){
        var uni = $("#uni").val();
        var password = $("#password").val();
        console.log(uni,'---',password);

        $.ajax({
            url: '/login',
            async: false,
            data: {
                'uni': uni,
                'password': password
            },
            success: function(result){

                // result --  (isGrader & uni) or error_msg
                for(var key in result){
                    if(key == 'error_msg'){ // no such user or wrong password
                        console.log("ERROR")
                        $("#error_msg").html(result.error_msg);
                    }
                }

                // successful log in
                console.log(result)
                // check if the current user is a student or a grader
                var isGrader = result.isGrader;
                if(!isGrader){ // is a student
                    userUNI = {
                        'uni': result.uni
                    }
                    location.href = "/show_student/"+ JSON.stringify(userUNI);
                    // $.post('/student_system', JSON.stringify(result));
                    // console.log('redirect')

                }
            },
            error: function(error) {
                console.log('Error!! ',JSON.stringify(error));
            }
        })
        return false;
    });
});