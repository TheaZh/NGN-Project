/**
 * Created by QW_Z on 11/7/17.
 */


/**************************************
 *
 *         Grade Nav Functions
 *
 **************************************/
function response_to_grade(course_id, uni) {
    //console.log('Response to Grade -- ', course_id);
    mute_content_title();
    $("#gradeData").empty();
    $.ajax({
        url: '/get_grade',
        async: false,
        data: {
            'course_id': course_id,
            'uni': uni
        },
        success: function(data) {
            // data{
            //      'grade': grade,
            //      'course_info': course_info,
            //      'grader': grader_name
            // }
            var course_info = data.course_info;
            var grade_table_title = '<i class="fa fa-check" id="couse-title"></i> ' +
                course_info.course_id + ' - ' +
                course_info.course_name;
            var grader = ' <span style="float: right;">Grader: ' + data.grader + '</span>'
            $("#table-course").empty();
            $("#table-course").append(grade_table_title + grader);
            //console.log(course_info.course_name);

            // grade is a dictionary -- 'assign_id' : [grade, comment]
            var grade = data.grade;
            var table_body = "";
            for (var key in grade) {
                var assign_id = key;
                if (grade.assign_id == null) {
                    var this_grade = 'None';
                    var this_comment = 'None';
                } else {
                    var this_grade = grade.assign_id[0];
                    var this_comment = grade.assign_id[1];
                }
                var assign_number = "Assignment" + assign_id.split("_A")[1];
                var html = '<tr>' +
                    '<td>' + assign_number + '</td>' +
                    '<td>' + this_grade + '</td>' +
                    '<td>' + this_comment + '</td>' +
                    '</tr>';

                table_body = table_body + html;
            }
            $("#gradeData").append(table_body);
        }
    });
    $("#gradeCard").css("display", "block");
}

function show_content_title() {
    $("#title-part").css("display", "block");
    // $("#content-title").css("display", "block");
    // $("#content-title-line").css("display", "block");
}

function mute_content_title() {
    $("#title-part").empty();
    $("#title-part").css("display", "none");
    // $("#content-title").css("display", "none");
    // $("#content-title-line").css("display", "none");
}

function mute_assignment_page() {
    $("#assignmentCard").css("display", "none");
    $("#assignment_title").empty();
    $("#assignment_description").empty();
}



/**************************************
 *
 *      Assignment Nav Functions
 *
 **************************************/

function mute_grade_page() {
    $("#title-part").css("display", "none");
    $("#gradeCard").css("display", "none");
}

function empty_assignment_cards() {
    $("#assignment_title").empty();
    $("#assignment_description").empty();
    $("#assignmentCard").css("display", "none");
}

function course_assignment(course_id, course_name) {
    empty_assignment_cards();
    // console.log('choose a course at Assignment Nav');
    // change subtitle and description
    $("#subtitle").text("Assignment  /  " + course_id + " - " + course_name);
    $("#title-part").empty();
    var description = '<br /><br /><p style="text-align: center"><i><b>' +
        'Select an assignment in the sidebar to view assignment description and submit files.' +
        '</b></i></p>';
    $("#title-part").append(description);
    $("#title-part").css("display", "block");
}

function response_to_assignment(uni, course_name, course_id, assignment_id) {
    course_assignment(course_id, course_name);
    mute_content_title();
    empty_assignment_cards();
    $.ajax({
        url: '/get_assignment',
        async: false,
        data: {
            'assignment_id': assignment_id
        },
        success: function(data) {
            /*
             * data -- assignment info
             */

            //********* Assignment title and description part ***********
            var assignment_num = data.assignment_id.split("_A")[1];
            var assignment_title = '<i class="fa fa-bookmark-o"></i>&ensp;Assignment ' + assignment_num;
            $("#assignment_title").append(assignment_title);

            // assignment description
            var assignment_description = data.description;
            var assign_description_html = '<p><i>Description:</i></p><p>' + assignment_description + '</p>';
            $("#assignment_description").append(assign_description_html);

            //********* Uploaded files list part ***********
            // manage card whose id is "#uploaded-file"
            var file_ids_list = data.uploaded_file_dict.uni;
            show_uploaded_files(file_ids_list);
        }
    });
    $("#assignmentCard").css("display", "block");
}

// show uploaded files list (not submitted)
function show_uploaded_files(file_ids_list) {
    // file_ids_list is a list of file-id that user uploaded for current assignment
    $.ajax({
        url: '/get_uploaded_files',
        async: false,
        data: {
            'file_ids_list': file_ids_list
        },
        success: function(files) {

        }
    });
}


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
            return false;
        }
    });

});
