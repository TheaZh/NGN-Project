/**
 * Created by QW_Z on 11/7/17.
 */

function response_to_grade(course_id, uni){
    console.log('Response to Grade -- ', course_id);
    $("#subtitle").text("Grade");
    $.ajax({
        url: '/get_grade/' + course_id + '/' + uni,
        success: function (grade) {
            // grade is a dictionary -- 'assign_id' : [grade, comment]
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
                console.log(assign_number);
                console.log(this_grade);
                console.log(this.comment);
                var html = '<tr>'
                        + '<td>' + assign_number + '</td>'
                        + '<td>' + this_grade + '</td>'
                        + '<td>' + this_comment + '</td>'
                        + '</tr>';

                table_body = table_body + html;
            }
            var table_title = '<thead><tr> <th>Assignment</th> <th>Score</th> <th>Comment</th></tr></thead>'
                            + '<tbody>' + table_body + '</tbody>';
            $("#dataTable").innerHTML(table_title);
            return false;
        }
    })
}

$(document).ready(function(){
    var uni = $("#userUNI").text();
    console.log('uni', uni);
    $.ajax({
        url: '/student_system/' + uni,
        success: function (data) {
            // data :  [user_data, courses_data]
            console.log('whole data: ',data);
            console.log('user data: ', data[0]);
            console.log('courses data: ', data[1]);
            console.log('---------');
            var user_data = data[0];
            var user_name = user_data.name;
            // show user name
            $("#user").text(user_name);

            // course_list
            course_data = data[1];
            var grade_list_html = "";
            var assign_list_html = "";
            for(var index in course_data){
                var tmp_course = course_data[index];
                console.log('course: ', tmp_course);
                // sort assignment list --> start from assignment 1
                var assign_list = tmp_course.assignment_list.sort();
                console.log('assign.list: ', assign_list);


                // for Assignments
                var sub_assign = "";
                for( var assign_index in assign_list){
                    var assignment = assign_list[assign_index];
                    console.log('assignment: ', assignment);
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
                console.log('$("#userUNI").text():', $("#userUNI").text());
                var parameters = tmp_course.course_id + ',' +  $("#userUNI").text();
                console.log("parameters: ", parameters);
                var tmp_html = '<li><a onclick="response_to_grade('+ tmp_course.course_id + ',' +  $("#userUNI").text()
                    +')">'
                    + tmp_course.course_id
                    + '</a></li>';
                grade_list_html = grade_list_html + tmp_html;
            }
            $("#Assignment").append(assign_list_html);
            $("#Grade").append(grade_list_html);
        }
    });
});