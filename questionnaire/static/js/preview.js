$(function(){
    disableInputFields(true);
    $('#edit_questionnaire_link').on('click', function(){
        disableInputFields(false);
    });
});

function disableInputFields(status) {
    $('.form-content :input[type=text],input[type=button],input[type=submit],input[type=radio],textarea').each(function () {
        $(this).prop('disabled', status);
    });
    $('.add-more').prop('disabled', status);
    var $upload_form_content = $('.upload_form_content');
    if (status)
        {$upload_form_content.hide();}
    else
        {$upload_form_content.show();}
}
