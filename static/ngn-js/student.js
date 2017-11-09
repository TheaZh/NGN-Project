/**
 * Created by QW_Z on 11/7/17.
 */

function response_to_grade(course_id, uni){
    //console.log('Response to Grade -- ', course_id);
    mute_content_title();
    $("#gradeData").empty();
    $("#gradeCard").css("display", "block");
    $.ajax({
        url: '/get_grade',
        data: {
            'course_id': course_id,
            'uni': uni
        },
        success: function (data) {
            // data{
            //      'grade': grade,
            //      'course_info': course_info,
            //      'grader': grader_name
            // }
            var course_info = data.course_info;
            var grade_table_title = '<i class="fa fa-check" id="couse-title"></i> '
                + course_info.course_id + ' - '
                + course_info.course_name;
            var grader = ' <span style="float: right;">Grader: ' + data.grader + '</span>'
            $("#table-course").empty();
            $("#table-course").append(grade_table_title + grader);
            //console.log(course_info.course_name);

            // grade is a dictionary -- 'assign_id' : [grade, comment]
            var grade = data.grade;
            var table_body = "";
            for( var key in grade){
                var assign_id = key;
                if (grade.assign_id == null){
                    var this_grade = 'None';
                    var this_comment = 'None';
                }
                else{
                    var this_grade = grade.assign_id[0];
                    var this_comment = grade.assign_id[1];
                }
                var assign_number = "Assignment" + assign_id.split("_A")[1];
                //console.log(assign_number);
                //console.log(this_grade);
                //console.log(this_comment);
                var html = '<tr>'
                    + '<td>' + assign_number + '</td>'
                    + '<td>' + this_grade + '</td>'
                    + '<td>' + this_comment + '</td>'
                    + '</tr>';

                table_body = table_body + html;
            }
            $("#gradeData").append(table_body);
        }
    })
}

function show_content_title(){
    $("#title-part").css("display", "block")
    // $("#content-title").css("display", "block");
    // $("#content-title-line").css("display", "block");
}

function mute_content_title(){
    $("#title-part").css("display", "none");
    // $("#content-title").css("display", "none");
    // $("#content-title-line").css("display", "none");
}

$(document).ready(function(){
    var uni = $("#userUNI").text();
    $("#gradeCard").css("display", "none");
    //console.log('uni', uni);

    // when click the "Grade" first level nav
    $("#grade-nav").click(function () {
        // change the subtitle name to 'Grade'
        $("#subtitle").text("Grade");
        // show content title with 'Grade'
        var description = '<br /><br /><p style="text-align: center"><i><b>' +
                            'Select a course in the sidebar to view assignment grade.' +
                            '</b></i></p>';
        // $("#content-title-line").append(description);
        $("#title-part").append(description);
        show_content_title();
    });

    $.ajax({
            url: '/student_system/' + uni,
            success: function (data) {
                // data :  [user_data, courses_data]
                //console.log('whole data: ',data);
                //console.log('user data: ', data[0]);
                //console.log('courses data: ', data[1]);
                //console.log('---------');
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
                for(var index in course_data){
                    var tmp_course = course_data[index];
                    //console.log('course: ', tmp_course);
                    // sort assignment list --> start from assignment 1
                    var assign_list = tmp_course.assignment_list.sort();
                    //console.log('assign.list: ', assign_list);


                    // for Assignments
                    var sub_assign = "";
                    for( var assign_index in assign_list){
                        var assignment = assign_list[assign_index];
                        //console.log('assignment: ', assignment);
                        var tmp_assign = '<li><a>Assignment ' + (parseInt(assign_index)+1) + '</a> </li>';
                        sub_assign = sub_assign + tmp_assign;
                    }
                    var assi_html = '<ul class="sidenav-third-level collapse" id="course'+index+'">' + sub_assign + '</ul>';
                    var cour_html = '<li><a class="nav-link-collapse collapsed" data-toggle="collapse" href="#course'+ index +'">'
                        + tmp_course.course_id + '</a>'
                        + assi_html
                        + '</li>';
                    assign_list_html = assign_list_html + cour_html;


                    // for Grades
                    //console.log('$("#userUNI").text():', $("#userUNI").text());
                    var tmp_html = '<li><a onclick="response_to_grade(\''+ tmp_course.course_id + '\',\'' +  ($("#userUNI").text()) + '\')'
                        +'">'
                        + tmp_course.course_id
                        + '</a></li>';
                    grade_list_html = grade_list_html + tmp_html;
                }
                //console.log('Append HTML');
                $("#Assignment").append(assign_list_html);
                $("#Grade").append(grade_list_html);
                return false;
            }
        });

});
