/**
 * Created by QW_Z on 11/7/17.
 */

/**************************************
 *
 *              Page
 *
 **************************************/
$(document).ready(function() {
    var uni = $("#userUNI").text();
    mute_assignment_page();
    mute_grade_page();
    //console.log('uni', uni);

    // ************ Grade page **************
    $("#grade-nav").click(function() {
        mute_assignment_page();
        $("#gradeCard").css("display", "none");
        mute_content_title();
        // change the subtitle name to 'Grade'
        $("#subtitle").text("Grade");
        // show brief description
        var description = '<br /><br /><p style="text-align: center"><i><b>' +
            'Select a course in the sidebar to view assignment grade.' +
            '</b></i></p>';
        $("#title-part").append(description);
        show_content_title();
    });

    // ************ Assignment page **************
    $("#assignment-nav").click(function() {
        mute_grade_page();
        mute_content_title();
        empty_assignment_cards();
        // change the subtitle name to 'Assignment'
        $("#subtitle").text("Assignment");
        // show brief description
        var description = '<br /><br /><p style="text-align: center"><i><b>' +
            'Select a course in the sidebar to view assignments.' +
            '</b></i></p>';
        $("#title-part").append(description);
        show_content_title();
    });

    // ************ Upload file Popup **************
    $("#choose_file_form").submit(function(){
        $.ajax({
            url: '/upload_files',
            type: 'POST',
            cache: false,
            async: false,
            data: new FormData($('#choose_file_form')[0]),
            processData: false,
            contentType: false,
            success:function(res){
                console.log(res);
                var message = res.msg;
                if(message == 'Please Select a File.'){
                    console.log('= =');

                    $("#choose_file_msg").empty()
                        .css("display", "block")
                        .append(message);
                }
                if(message == 'Successful Uploaded!'){
                    close_choose_file_window();
                    response_to_assignment(uni, cur_course_name, cur_course_id, cur_assignment_id);
                }
            },
            error: function(res){
                console.log(res);
            }
        });
        return false;
    });



    // ************ Data Fetching ****************
    $.ajax({
        url: '/student_system/' + uni,
        async: false,
        success: function(data) {
            var user_data = data[0];
            var user_name = user_data.name;
            var show_user_html = '<i class="fa fa-fw fa-user-o"></i>' + user_name;
            // show user name
            $("#user").empty();
            $("#user").append(show_user_html);

            // course_list
            var course_data = data[1];
            var grade_list_html = "";
            var assign_list_html = "";

            // ****** Build Sidebar ********
            for (var index in course_data) {
                /*
                 *  tmp_course -----> current course info from database
                 */
                var tmp_course = course_data[index];
                //console.log('course: ', tmp_course);
                // sort assignment list --> start from assignment 1
                var assign_list = tmp_course.assignment_list.sort();
                //console.log('assign.list: ', assign_list);


                // for Assignments
                var sub_assign = "";
                for (var assign_index in assign_list) {
                    var assignment = assign_list[assign_index]; // this is assignment id
                    // console.log('assignment: ', assignment);
                    // var para = {
                    //     'course_name': tmp_course.course_name,
                    //     'course_id': tmp_course.course_id,
                    //     'assignment': assignment
                    // }
                    // console.log('html - onclick -- assignment_id: ', para);
                    var tmp_assign = '<li><a onclick="response_to_assignment(\'' +
                        uni + '\',\'' + tmp_course.course_name + '\',\'' +
                        tmp_course.course_id + '\',\'' + assignment +
                        '\')">' +
                        'Assignment ' + (parseInt(assign_index) + 1) +
                        '</a> </li>';
                    sub_assign = sub_assign + tmp_assign;
                }
                // third level nav -- assignment list under course nav
                var assi_html = '<ul class="sidenav-third-level collapse" id="course' + index + '">' + sub_assign + '</ul>';
                // seconde level nav -- course list under Assignment
                var cour_html = '<li><a class="nav-link-collapse collapsed" data-toggle="collapse" ' +
                    'onclick="course_assignment(\'' + tmp_course.course_id +
                    '\',\'' + tmp_course.course_name +
                    '\')" ' +
                    'href="#course' + index + '">' +
                    tmp_course.course_id + '</a>' + assi_html + '</li>';
                assign_list_html = assign_list_html + cour_html;


                // for Grades
                //console.log('$("#userUNI").text():', $("#userUNI").text());
                var tmp_html = '<li><a onclick="response_to_grade(\'' + tmp_course.course_id + '\',\'' + ($("#userUNI").text()) + '\')' +
                    '">' +
                    tmp_course.course_id +
                    '</a></li>';
                grade_list_html = grade_list_html + tmp_html;
            }
            //console.log('Append HTML');
            $("#Assignment").append(assign_list_html);
            $("#Grade").append(grade_list_html);
        }
    });


});
