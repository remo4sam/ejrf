$(function(){
    $('#preview_modal').on('show.bs.modal', function(){
        var questionnaire_id = $(this).attr('data-attribute-id');
        var questionnaire_preview_url = "/questionnaire/preview/"+questionnaire_id;
        $.get(questionnaire_preview_url, function( data ) {
            var $holder = $('<div></div>').append(String(data));
            var content =  $holder.find("#preview-content").html()
            $( "#ajax-content" ).html(content);
            disable_modal_input_fields();
        });
    });
    disable_modal_input_fields();

    $('#edit_questionnaire_link').on('click', function(){
        disableInputFields();
    });

    $('.assign-question').on('show.bs.modal', function(){
        var subsection_id = $(this).attr('subsection-id'),
            assign_to_subsection_url = "/subsection/" + subsection_id +"/assign_questions/";
        $.get(assign_to_subsection_url, function( data ) {
            var $holder = $('<div></div>').append(String(data));
            var content =  $holder.find("#question-list").html()
            $( "#assign-question-ajax-content-"+subsection_id ).html(content);
        });
    });

    $('.edit_section').on('show.bs.modal', function(){
        var section_id = $(this).attr('object-id'),
            assign_to_subsection_url = "/section/" + section_id +"/edit/";
        $.get(assign_to_subsection_url, function( data ) {
            var $holder = $('<div></div>').append(String(data));
            var content =  $holder.find("#form-content").html()
            $( "#edit_section_"+section_id+"_ajax_content").html(content);
            $('textarea').autosize();
        });
    });


});

function disable_modal_input_fields(){
    $('.preview-content :input').each(function() {
       $(this).attr('disabled','disabled');
    });
};

function disableInputFields(status) {
    $('.form-content :input').each(function () {
        $(this).prop('disabled', status);
    });
    $('.add-more').prop('disabled', status);
}