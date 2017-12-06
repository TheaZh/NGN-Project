/**
 * Created by eAson on 2017/11/13.
 */

// set global assignment_id
var g_assignment_id='';


$(function(){
    var uni=$("#userUNI").text();
    console.log(uni);
    var description = '<br /><br /><p style="text-align: center"><i><b>' +
            'Select a course in the sidebar to grade assignments.' +
            '</b></i></p>';
    $('#title-part').append(description).css('display', 'block');


    // data fetching & builder nav bar
    $.ajax({
            url: '/grader_system',
            async: false,
            success: function (data) {
                var user_data = data[0];
                var user_name = user_data.name;
                var show_user_html = '<i class="fa fa-fw fa-user-o"></i>' + user_name;

                // show user name
                $("#user").empty();
                $("#user").append(show_user_html);

                // data=[user_data, course_data]
                var course_data = data[1];
                var assign_list_html = "";
                console.log('course_data:', course_data);

                // ****** Build Sidebar ********
                for (var index in course_data) {
                    /*
                     *  tmp_course -----> current course info from database
                     */
                    var tmp_course = course_data[index];
                    console.log('index: ', index);
                    //console.log('course: ', tmp_course);
                    // sort assignment list --> start from assignment 1
                    var assign_list = tmp_course['assignment_list'].sort();
                    console.log('assign.list: ', assign_list);


                    // for Assignments
                    var sub_assign = "";
                    for (var assign_index in assign_list) {
                        var assignment = assign_list[assign_index]; // this is assignment_id
                        // console.log('assignment: ', assignment);
                        // var para = {
                        //     'course_name': tmp_course.course_name,
                        //     'course_id': tmp_course.course_id,
                        //     'assignment': assignment
                        // }
                        // console.log('html - onclick -- assignment_id: ', para);
                        var tmp_assign = '<li><a onclick="response_to_grader(\''+ assignment + '\')">' +
                            'Assignment ' + (parseInt(assign_index) + 1) +
                            '</a> </li>';
                        sub_assign = sub_assign + tmp_assign;
                    }
                    // third level nav -- assignment list under course nav
                    var assi_html = '<ul class="sidenav-third-level collapse" id="course' + index + '">' + sub_assign + '</ul>';
                    // second level nav -- course list under Assignment
                    var cour_html = '<li><a class="nav-link-collapse collapsed" data-toggle="collapse" ' +
                        'href="#course' + index + '">' +
                        tmp_course.course_id + '</a>' + assi_html + '</li>';
                    assign_list_html = assign_list_html + cour_html;
                }
                $('#Course').append(assign_list_html);
                return false;
            }
        });

    // submit form
    $('#myForm').submit(function(){
        $.ajax({
            url: '/post',
            data:{
                'uni': $('#formUni').val(),
                'grade': $('#formGrade').val(),
                'comment': $('#formComment').val(),
                'assignment_id': $('#formAssignment').val()
            },
            success: function(){
                $('#myModal').modal('hide');
                $('#success_modal').modal('show');
                return false;
            }
        })
    });

    // data fetching & build toBeGraded datatables
    $('#tab1').click(function () {
        console.log('click triggered');
        console.log(g_assignment_id);
        $.ajax({
            url: '/get_assignment',
            data: {'assignment_id': g_assignment_id},
            success: function (data) {

                // refresh current datatable
                $('#ToBeGradedList').dataTable().fnDestroy();

                // refresh current table
                $('#tb1').empty();

                var ToBeGradedList_html = "";
                var submitted_file_dict = data['submitted_file_dict'];
                // for (var key in submitted_file_dict) {
                //     ToBeGradedList_html = ToBeGradedList_html + '<tr>' +
                //         '<td>' + key + '</td>' +
                //         '<td><button class="btn btn-info" onclick="download(\''+ key +
                //         '\', \''+ g_assignment_id +'\')">Download</button></td>' +
                //         '<td><button class="btn btn-primary"' + ' onclick="set_uni(\'' + key +
                //         '\', \'' + g_assignment_id + '\')" data-toggle="modal" data-target="#myModal">' +
                //         'Grade</button></td>' +
                //         '</tr>'
                // }
                for (var key in submitted_file_dict) {
                    ToBeGradedList_html = ToBeGradedList_html + '<tr>' +
                        '<td><b>' + key + '</b></td>' +
                        '<td><a class="btn mt-0 btn-sm btn-info" href="/download_file/'+key + '/'+g_assignment_id+'">Download</a></td>' +
                        '<td><button class="btn mt-0 btn-sm btn-primary"' + ' onclick="set_uni(\'' + key +
                        '\', \'' + g_assignment_id + '\')" data-toggle="modal" data-target="#myModal">' +
                        'Grade</button></td>' +
                        '</tr>';

                }

                key='test';
                $('#tb1').append(ToBeGradedList_html);

                // build datatable
                $('#ToBeGradedList').dataTable({
                    ordering: false
                });
            }
        });
    });

    // build Graded datatable
    $('#tab2').click(function () {
        $.ajax({
            url: '/grader_view',
            data: {'assignment_id': g_assignment_id},
            success: function (data) {

                // refresh current datatable
                $('#GradedList').dataTable().fnDestroy();

                // refresh current table
                $('#tb2').empty();


                if(!$.isEmptyObject(data)) {
                    var GradedList_html = "";
                    for (var key in data) {
                        GradedList_html = GradedList_html +
                            '<tr>' +
                            '<td>' + key + '</td>' +
                            '<td>' + data[key][0] + '</td>' +
                            '<td>' + data[key][1] + '</td>' +
                            '</tr>'
                    }

                    $('#tb2').append(GradedList_html);
                    // build datatable

                }
                $('#GradedList').dataTable({
                    ordering: false
                });
            }
        });
    });


});

/**************************************
 *
 *     Grader Nav Functions
 *
 **************************************/

function response_to_grader(assignment_id) {

    // set current global assignment_id
    g_assignment_id=assignment_id;

    // mute #title-part
    mute_content_title();

    // show assignment title
    var course_name = assignment_id.split('_')[0] + '  Assignment';
    var assignment_num = assignment_id.split("_A")[1];
    var assignment_title = '<i class="fa fa-bookmark-o"></i>&ensp; ' + course_name + ' ' + assignment_num;
    // $('#grading-assign-title').empty().append(assignment_title);
    $("#subtitle").text("Grade  /   " + course_name + " " + assignment_num);
    $('#myTab').css('display', 'block');

    // manually set a 'click' event
    $('#tab1').trigger('click');

}

function set_uni(uni, assignment_id) {

    $('#formUni').attr({
        "value" : uni
    });
    $('#formAssignment').attr({
        "value" : assignment_id
    });

}

function download(uni, assignment_id) {
    $.ajax({
        url: '/download_file',
        async: false,
        data: {
            'uni': uni,
            'assignment_id': assignment_id
        },
        success: function(result){
            window.open(result);
        }
    });
}
