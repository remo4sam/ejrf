var form_has_changed = false;
var editable = false;

$(document).ready(function() {
    $('.pagination').children('ul').addClass('pagination')
    $('a[data-toggle=popover]').popover();
    loadRoleTemplate();
    $('p:empty').remove();

    $('.datetimepicker').datetimepicker({ pickTime: false });
    $('textarea').autosize();

    $('.grid-error').hover(function(){
        $(this).popover('show');}, function(){
        $(this).popover('hide');
    });
});

function cloneMore(selector) {
    $('a[data-toggle=popover]').popover('destroy');
    $('textarea').trigger('autosize.destroy');
    $('.datetimepicker').each(function(){
        $(this).data("DateTimePicker").destroy();
    });

    var newElement = $(selector).clone(true);
    updateFormCounts(newElement);

    newElement.find(':input').each(function() {
        // Reset cloned inputs
        if($(this).attr('type') != 'radio')
            $(this).val('');

        $(this).removeAttr('checked');
        $(this).removeAttr('selected');
    });

    $(selector).after(newElement);
    $(selector).after('<button type="button" class="btn btn-default red delete-more close">×</button>');
    $(selector).after("<hr class='multiple-hr'/>");

    $('a[data-toggle=popover]').popover();
    $('textarea').autosize().trigger('autosize.resize');
    $('.datetimepicker').datetimepicker({ pickTime: false });
}

function updateFormCounts(form_element){
    form_element.find(':input').each(function() {
        var inputType = $(this).attr('name').split('-', 1)[0];
        var total = $('#id_' + inputType + '-TOTAL_FORMS').val();

        var name = $(this).attr('name').replace(/-[\d]+-/g, '-'+total.toString()+'-');
        var id = $(this).attr('id').replace(/-[\d]+-/g, '-'+total.toString()+'-');
        $(this).attr({'name': name, 'id': id})

        if($(this).attr('type') == 'radio'){
            //update the previous label
            $(this).parents('label').attr({'for': id});

            //update count if gone through all the ul elements
            var list_count = $(this).parents('ul')[0].childElementCount;
            var element_count = parseInt(id.substr(id.length - 1)) + 1;
            if(list_count == element_count)
                total++;
        }
        else
            total++;

        $('#id_' + inputType + '-TOTAL_FORMS').val(total);
        $('#id_' + inputType + '-MAX_NUM_FORMS').val(total);
    });
}

$('.add-more').on('click', function(event) {
    cloneMore($(this).prev('.question-group'));
});

$('textarea').on('keyup', function(event){
  var maxLength = 256;
  if($(this).val().length >= maxLength)
    $(this).val($(this).val().substring(0, maxLength));
});

$(document).on('click', '.delete-more', function() {
    $('a[data-toggle=popover]').popover('destroy');

    $(this).next('.question-group').remove();
    $(this).prev('.multiple-hr').remove();
    $(this).remove();

    $('a[data-toggle=popover]').popover();
});


$('#export-section').on('click', function(event) {
    $(this).toggleClass('active');
    var filename = "";
    $.ajax({
        type: "GET",
        async: false,
        url: "/export-section",
        success: function(data){
            var obj = JSON.parse(data);
            filename = obj['filename']
        }
    });

    setTimeout(function(){
      $('#export-section').toggleClass('active');
      return_file(filename)
    }, 8000);
});

function return_file(filename){
    window.location = "/export-section/"+filename;
}

$('#id-older-jrf').on('click', function(event) {
    $('.hide').toggleClass('show');
    $(this).html($(this).html() === "More" ? "Less" : "More");
    event.preventDefault()
});

function disableInputFields(status) {
    $(this).find('.form-content :input').each(function () {
        $(this).prop('disabled', status);
    });
    $('.add-more').prop('disabled', status);
}

$('.unassign-question').hover(function(){
    var parent_question = $(this).parents('div[class^="form-group"]');
    $(parent_question).toggleClass('question-form');
});