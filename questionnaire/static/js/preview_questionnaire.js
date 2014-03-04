$(function(){
    $('#preview_modal').on('show.bs.modal', function(){
        $.post( location.pathname, $( "#questionnaire_entry" ).serialize() );
        var questionnaire_preview_url = get_questionnaire_preview_url($(this));
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

});

function get_questionnaire_preview_url($element){
        var questionnaire_id = $element.attr('data-attribute-id');
        var questionnaire_preview_url = "/questionnaire/"+ questionnaire_id + "/preview/";
        return questionnaire_preview_url.replace('//', '/')
}

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