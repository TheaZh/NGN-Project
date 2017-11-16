var uni = $("#userUNI").text();
var cur_course_id = '';
var cur_course_name = '';
var cur_assignment_id = '';

/**************************************
 *
 *     Files operation Functions
 *
 **************************************/
// upload files from users disk
function choose_files() {
    // PopUp
    $("#pop-up-div").css("display", "block");
}
// close file choose window and reset the form
function close_choose_file_window(){
    $("#pop-up-div").css("display", "none");
    $("#choose_file_form")[0].reset();
    $("#choose_file_msg").empty();
}


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
    cur_course_id = course_id;
    cur_course_name = course_name;
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
    cur_assignment_id = assignment_id;
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
            console.log('data:',data);
            // console.log('cur uni:', uni);
            console.log(data.upload_file_dict);
            var file_ids_list = [];
            if(uni in data.upload_file_dict){
                file_ids_list = data.upload_file_dict[uni];
            }
            console.log('uni - file_ids_list:', uni, ' -- ', file_ids_list);
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
            'file_ids_list': JSON.stringify(file_ids_list)
        },
        success: function(file_name_dict) {
            console.log('file_name_dict:', file_name_dict);
            // file name dict -- key: filename_version, value: file_id('_id')
            var file_list_html = '';
            for(var file in file_name_dict){
                // console.log('file item: ', file);
                // console.log('file item: ', file_name_dict[file]);
                console.log('file item: ', file_name_dict[file][1]);
                // var file_html = '<label class="ml-2 form-check-label"><input class="form-check-input" type="checkbox" value='+ file_name_dict.file + '>'+ file +'</label><br>'

                var file_html = '<tr>' +
                                '<td>' + file + '</td>' +
                                ' <td>'+ file_name_dict[file][1] + '</td>' +
                                '<td><label class="form-check-label"><input type="checkbox" value='+ file_name_dict[file][0] + '></label>'+
                                '</td>' +
                                '</tr>';

                file_list_html = file_list_html + file_html;
            }
            var file_list_table =   '<form>' +
                                    '<table class="table table-sm">'+
                                    '<thead>'+
                                    '<tr>'+
                                    '<th>File Name</th>'+
                                    '<th>Timestamp</th>'+
                                    '<th>Submit</th>'+
                                    '</tr>'+
                                    '</thead>' +
                                    '<tbody>' +
                                    file_list_html +
                                    '</tbody>' +
                                    '</table>'+
                                    '</form>';
            if (file_list_html == ''){
                file_list_table = file_list_table + '<p class="text-muted" style="text-align: center"><i>None</i><p>';
            }
            $("#uploaded-file").empty().append(file_list_table);
        }
    });
}
