var uni = $("#userUNI").text();
var cur_course_id = '';
var cur_course_name = '';
var cur_assignment_id = '';

/**************************************
 *
 *     Files operation Functions
 *
 **************************************/
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
            //console.log("Grade:", grade);
            var table_body = "";
            for (var key in grade) {
                var assign_id = key;
                //console.log(grade[assign_id]);
                if (grade[assign_id].length <=0) {
                    var this_grade = 'None';
                    var this_comment = 'None';
                } else {
                    var this_grade = grade[assign_id][0];
                    var this_comment = grade[assign_id][1];
                }
                //console.log('This Grade:', this_grade);
                //console.log('This comment:', this_comment);
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
            //console.log('data:',data);
            // //console.log('cur uni:', uni);
            //console.log(data.upload_file_dict);
            var file_ids_list = [];
            if(uni in data.upload_file_dict){
                file_ids_list = data.upload_file_dict[uni];
            }
            //console.log('uni - file_ids_list:', uni, ' -- ', file_ids_list);
            show_uploaded_files(file_ids_list);
            var submitted_file_ids = [];
            var submission_timestamp = '';
            if(uni in data.submitted_file_dict){
                submitted_file_ids = data.submitted_file_dict[uni][0];
                submission_timestamp = data.submitted_file_dict[uni][1];
            }
            // console.log('uni - submitted_file_ids:', uni, ' -- ', submitted_file_ids);
            show_submitted_files(submitted_file_ids, submission_timestamp);
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
            // console.log('file_name_dict:', file_name_dict);
            // file name dict -- key: filename_version, value: file_id('_id')
            var file_list_html = '';
            for(var file in file_name_dict){
                // console.log('file item: ', file);
                // console.log('file item: ', file_name_dict[file]);
                // console.log('file item: ', file_name_dict[file][1]);
                // var file_html = '<label class="ml-2 form-check-label"><input class="form-check-input" type="checkbox" value='+ file_name_dict.file + '>'+ file +'</label><br>'

                var file_html = '<tr>' +
                                '<td><a href="/download_from_cloud/' + file_name_dict[file][0] +'">' + file + '</a></td>' +
                                '<td class="text-muted"><i>'+ file_name_dict[file][1] + '</i></td>' +
                                '<td><label class="form-check-label">'+
                                '<input name="choose-submit" type="checkbox" value='+ file_name_dict[file][0] +
                                '></label>'+
                                '</td>' +
                                '</tr>';

                file_list_html = file_list_html + file_html;
            }

            $("#uploaded-file-table-body").empty().append(file_list_html);
        }
    });
}


// show submitted files
function show_submitted_files(submitted_file_ids, submission_timestamp){
    //console.log('submit--', submission_timestamp);
    $("#submitted-list").empty();
    if(submission_timestamp != ''){
        $.ajax({
            url:'/get_submitted_files',
            data:{
                'submitted_file_ids': JSON.stringify(submitted_file_ids)
            },
            success: function(submitted_file_name_dict){
                // submitted_file_name_dict -- key: file_name, val: file_id
                //console.log('submitted_file_name_dict:',submitted_file_name_dict);
                var sub_file_list_html = ''
                var timestamp_html = '<p class="text-muted"><i>Submitted at: '+ submission_timestamp +'</i></p>';
                for(var file_name in submitted_file_name_dict){
                    sub_file_list_html += '<p class="mt-0 mb-0">' + file_name + '</p>';
                }
                sub_file_list_html = timestamp_html + sub_file_list_html;
                $("#submitted-list").empty().append(sub_file_list_html);
            }
        });
    }
}


// submit choson files in the "uploaded files" zone
function submit_files(){
    //console.log('ready to submit...');
    // document.getElementById("submitting-file").submit()
    var chosen_file_id = document.getElementsByName("choose-submit");
    var submit_list = []
    for(var id in chosen_file_id){
        if(chosen_file_id[id].checked){
            //console.log(chosen_file_id[id].value);
            submit_list.push(chosen_file_id[id].value);
        }
    }
    if(submit_list.length !=0){
        //console.log('new submit list: ', submit_list);
        $.ajax({
            url: '/submit_files',
            data: {
                'submit_id_list': JSON.stringify(submit_list)
            },
            success: function(msg){
                //console.log("submitted message:", msg);
            }
        });
        response_to_assignment(uni, cur_course_name, cur_course_id, cur_assignment_id);
    }
    else{
        //console.log('no submit file chosen');
    }
}

// delete uploaded files
function delete_files(){
    var chosen_file_id = document.getElementsByName("choose-submit");
    var delete_list = []
    for(var id in chosen_file_id){
        if(chosen_file_id[id].checked){
            //console.log(chosen_file_id[id].value);
            delete_list.push(chosen_file_id[id].value);
        }
    }
    if(delete_list.length !=0){
        //console.log('new submit list: ', submit_list);
        $.ajax({
            url: '/delete_files',
            data: {
                'delete_id_list': JSON.stringify(delete_list)
            },
            success: function(msg){
                console.log("submitted message:", msg);
                message = ''
                if(msg.msg.length <= 0){
                    // delete successfully
                    message = 'Deleted selected files!';
                    console.log(message);
                }
                else{
                    message = msg.msg;
                    console.log(message);
                }
                $("#delete_file_span").empty().append(message);
            }
        });
        response_to_assignment(uni, cur_course_name, cur_course_id, cur_assignment_id);
    }
    else{
        $("#delete_file_span").empty().append('No File Choosen!');
    }
}
