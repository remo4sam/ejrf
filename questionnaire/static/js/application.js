var form_has_changed = false;
var editable = false;

$(document).ready(function() {
    $('.pagination').children('ul').addClass('pagination')
    $('a[data-toggle=popover]').popover();
    $('a[data-toggle=tooltip]').tooltip();
    loadRoleTemplate();
    $('p:empty').remove();

    $('.datetimepicker').datepicker({ pickTime: false, autoclose: true });
    $('textarea').autosize();

    $('.grid-error').hover(function(){
        $(this).popover('show');}, function(){
        $(this).popover('hide');
    });

    $('#first_row').find('input[type=hidden]').each(function(index, element){
            $(element).val(0);
        });
});

function replaceAttributes($el, index) {
    return {'name': _replace($el, 'name', index),
            'id': _replace($el, 'id', index)};
}

function _replace($el, attr, index){
    return $($el).attr(attr).replace(/-[\d]+-/g, '-'+ index.toString()+'-')
}

function reIndexFieldNames() {
    var fieldTypes = ['MultiChoice', 'Date', 'Number', 'Text'];
    fieldTypes.forEach(function(type){
        var total = -1;
        var previous_name = '';
        $('#questionnaire_entry').find(":input[name^=" + type + "][type!=hidden]").each(function(index, el){
            var $el = $(el),
                name = $el.attr('name'),
                type = $el.attr('type');
            if (!(previous_name == name && type == 'radio')){
                total = total +1;
            }
            var attributeMap = replaceAttributes($el, total);
            $el.attr({'name': attributeMap.name, 'id': attributeMap.id});
            var $hidden = $el.prev("input[name="+ name +"]");
            $hidden.attr({'name': attributeMap.name, 'id': attributeMap.id});
            previous_name = name;
        });
        $('#id_' + type + '-MAX_NUM_FORMS').val(total+1);
        $('#id_' + type + '-INITIAL_FORMS').val(total+1);
        $('#id_' + type + '-TOTAL_FORMS').val(total+1);
    });
}

function removeUsedOptions(new_row, $table) {
    var  new_row_primary_select = new_row.find('select').first();
    $table.find('tbody tr').each(function(){
       var used_option = $(this).find("td:eq(1)").find("select").find("option:selected");
       new_row_primary_select.find('option[value='+ used_option.val() + ']').remove();
    });
    new_row_primary_select.append('<option value="">Choose One</option>');
    new_row.find(':input[type!=hidden]').each(function(){
        $(this).val('');
    });
}

function prependHiddenColumnFields(newElement) {
    newElement.find(':input').each(function(){
        var $el = $(this);
        var name = $el.attr('name');
        $el.before('<input type="hidden" name="' + name + '" />')
    });
}

function AddRow(selector) {
    var $selector = $(selector);
    var newElement = $selector.clone(true);
    newElement.find('input[type=hidden]').each(function(){ $(this).remove()});
    newElement.find('.primary-question').each(function(){ $(this).removeAttr('data-primary-question')});
    prependHiddenColumnFields(newElement);
    $selector.after(newElement);
    var $table = $selector.parents('table');
    assignRowNumbers($table);
    removeUsedOptions(newElement, $table);
    reIndexFieldNames();
    resetDatePicker(newElement);
}

function assignRowNumbers($table){
    $table.find("span.number").each(function(i, element){
        $(element).text(++i);
    });
}

function addDeleteMoreButton(selector) {
    var $selector = $(selector);
    $selector.after('<button type="button" class="btn btn-default red delete-more close">×</button>');
    $selector.after("<hr class='multiple-hr'/>");
}

function resetDatePicker(newElement) {
    newElement.find('.datetimepicker').each(function(){
        var $this = $(this);
        $this.removeData('datepicker').unbind();
        $this.datepicker({ pickTime: false, autoclose: true });
    });
}

function cloneMore(selector) {
    var newElement = getClone(selector);
    $(selector).after(newElement);
    addDeleteMoreButton(selector);
    resetClonedInputs(newElement);
    resetDatePicker(newElement);
}

function resetClonedInputs(newElement){
    newElement.find(':input').each(function() {
        if($(this).attr('type') != 'radio')
            $(this).val('');
        $(this).removeAttr('checked');
        $(this).removeAttr('selected');
    });
}

function getClone(selector){
    return $(selector).clone(true);
}

$('.add-more').on('click', function(event) {
    cloneMore($(this).parents('.question-group'));
    reIndexFieldNames();
    event.preventDefault();
});

function addRowAndColumnHiddenInputs($table, group_id) {
    $table.find('tr').each(function(i, el){
        var $tr = $(this);
        $tr.find('input[type=hidden]').each(function(index, element){
            $(element).val([i, group_id]);
        });
    });
}

$('.add-row').on('click', function(event) {
    var $grid_row = $(this).parents('tr').prev();
    AddRow($grid_row);
    var $table = $(this).parents('table');
    var group_id = $table.attr('data-group-id');
    addRowAndColumnHiddenInputs($table, group_id);
});

$('textarea').on('keyup', function(){
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
    event.preventDefault();
});

function return_file(filename){
    window.location = "/export-section/"+filename;
}

$('#id-older-jrf').on('click', function(event) {
    $('.hide').toggleClass('show');
    $(this).html($(this).html() === "More" ? "Less" : "More");
    event.preventDefault()
});

$('.unassign-question').hover(function(){
    var parent_question = $(this).parents('div[class^="form-group"]');
    $(parent_question).toggleClass('question-form');
});

$('.remove-table-row').on('click', function(evt){
    var $row = $(this).parents('tr'),
        $table = $row.parents('table'),
        $grid_rows = $table.find('tr.grid_row');

    if ($grid_rows.length > 1){
        deleteRowFromServer($row, $table);
        $row.remove();
        assignRowNumbers($table);
        reIndexFieldNames();
    }
    evt.preventDefault();
});

function deleteRowFromServer($row,$table) {
    var group_id = $table.attr('data-group-id');
    var url = window.location.pathname + "delete/" + group_id + "/";
    var $primary_answer = $row.find('.primary-question').attr('data-primary-question'),
        $csrf = $('input[name=csrfmiddlewaretoken]'),
        data = {'primary_answer': $primary_answer, 'csrfmiddlewaretoken': $csrf.val()};
    if ($primary_answer){
        $.post(url, data, function(){});
    };
}
