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
            data: {
                'uni': uni,
                'password': password
            },
            success: function(result){
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
                if(!isGrader){
                    console.log(result.course_list)
                    $.ajax({
                        url: '/student_system',
                        data: {
                            'student_data' : JSON.stringify(result)
                        },
                        success: function (result) {
                            localStorage.setItem('courseData', result);
                            window.location.href = "http://www.baidu.com";
                        }
                    });
                }

            },
            error: function(error) {
                console.log('Error!! ',JSON.stringify(error));
            }
        })

    });
});