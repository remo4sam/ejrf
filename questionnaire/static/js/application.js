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
            if(previous_name !=name && type == 'radio'){
                var $radio_extra_hidden = $el.prev().prev("input[name="+ name +"]");
                $radio_extra_hidden.attr({'name': attributeMap.name, 'id': attributeMap.id});
            }
            var $label = $el.parents("label");
            $label.attr('for', attributeMap.id);
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
    var previous_name = '';
    newElement.find(':input').each(function(){
        var $el = $(this);
        var name = $el.attr('name'),
            type = $el.attr('type');
        if (!(previous_name == name && type == 'radio')){
            $el.before('<input type="hidden" name="' + name + '" />')
        }
        if(previous_name !=name && type == 'radio'){
            $el.before('<input type="hidden" exclude="true" value="" name="' + name + '" />')
        }
        previous_name = name;
    });
}

function duplicateRow(selector, $table) {
    var $selector = $(selector);
    var newElement = $selector.clone(true);
    newElement.find('input[type=hidden]').each(function(){ $(this).remove()});
    newElement.find('.primary-question').each(function(){ $(this).removeAttr('data-primary-question')});
    resetClonedInputs(newElement);
    prependHiddenColumnFields(newElement);
    $selector.after(newElement);
    assignRowNumbers($table);
    removeUsedOptions(newElement, $table);
    reIndexFieldNames();
    resetDatePicker(newElement);
    return newElement;
}

function assignRowNumbers($table){
    $table.find("span.number").each(function(i, element){
        $(element).text(++i);
    });
}

function showSeparator($selector) {
    var separator = $selector.find('.separator');
    separator.removeClass('hide');
    separator.show();
}

function resetDatePicker(newElement) {
    newElement.find('.datetimepicker').each(function(){
        var $this = $(this);
        $this.removeData('datepicker').unbind();
        $this.datepicker({ pickTime: false, autoclose: true });
    });
}

function resetClonedInputs(newElement){
    newElement.find(':input').each(function() {
        if($(this).attr('type') != 'radio')
            $(this).val('');
        $(this).removeAttr('checked');
        $(this).removeAttr('selected');
    });
}

function addRowAndColumnHiddenInputs($table, group_id, row_selector) {
    $table.find(row_selector).each(function(i, el){
        var $tr = $(this);
        $tr.find('input[type=hidden][exclude!=true]').each(function(index, element){
            $(element).val([i, group_id]);
        });
    });
}

function addRowOn($el, row_selector, table_selector) {
    var $grid_row = $el.parents(row_selector).prev();
    var $table = $el.parents(table_selector);
    var $new_row = duplicateRow($grid_row, $table);
    var group_id = $table.attr('data-group-id');
    addRowAndColumnHiddenInputs($table, group_id, row_selector);
    return $new_row;
}

$('input[type=radio]').on('click', function(){
    var $el = $(this),
        name = $el.attr('name'),
        $redundant_hidden_radio = $el.parents('.form-group').find('input[name='+ name +'][exclude=true]');
    $redundant_hidden_radio.remove();
});

$('.add-row').on('click', function(event) {
    var $el = $(this);
    addRowOn($el, 'tr', 'table');
    event.preventDefault();
});

$('.add-more').on('click', function(event) {
    var $el = $(this);
    var $new_row = addRowOn($el, '.hybrid-group-row', '.question-group');
    showSeparator($new_row);
    event.preventDefault();
});

$('textarea').on('keyup', function(){
  var maxLength = 256;
  if($(this).val().length >= maxLength)
    $(this).val($(this).val().substring(0, maxLength));
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

function disableInputFields(status) {
    $(this).find(":input").each(function () {
        $(this).prop('disabled', status);
    });
    $('.add-more').prop('disabled', status);
}

$('.unassign-question').hover(function(){
    var parent_question = $(this).parents('div[class^="form-group"]');
    $(parent_question).toggleClass('question-form');
});

$('.remove-table-row').on('click', function(evt){
    var $row = $(this).parents('tr'),
        $table = $row.parents('table'),
        $grid_rows = $table.find('tr.grid_row');
    deleteRow($row, $table, $grid_rows, 1);
    evt.preventDefault();
});

$('.remove-hybrid-row').on('click', function(evt){
    var $row = $(this).parents('.hybrid-group-row'),
        $table = $row.parents('.question-group'),
        $grid_rows = $table.find('.hybrid-group-row');
    deleteRow($row, $table, $grid_rows, 2);
    evt.preventDefault();
});

function deleteRow($row, $table, $grid_rows, min_number_of_rows) {
    if ($grid_rows.length > min_number_of_rows){
        deleteRowFromServer($row, $table);
        $row.remove();
        assignRowNumbers($table);
        reIndexFieldNames();
    }
}

function deleteRowFromServer($row,$table) {
    var group_id = $table.attr('data-group-id');
    var url = window.location.pathname + "delete/" + group_id + "/";
    var $primary_answer = $row.find('.primary-question').attr('data-primary-question'),
        $csrf = $('input[name=csrfmiddlewaretoken]'),
        data = {'primary_answer': $primary_answer, 'csrfmiddlewaretoken': $csrf.val()};
    if ($primary_answer){
        $.post(url, data, function(){});
    }
}


function getModalWithSubSectionQuestions($element) {
    var data = $element.parents('div .subsection-content').html(),
        $modal = $('#reorder_modal_label'),
        action = $element.attr('data-href');
        $modal.find('#content').html(data);
            $modal.find('#re-order-questions-form').attr('action', action);
    return $modal;
}

function removeButtons($modal, btnClasses) {
    btnClasses.forEach(function(btn){
       $modal.find(btn).remove();
    });
}

function highlightOnHover($modal) {
    $modal.find('table tr').each(function(){
        $(this).hover(function(){
            $(this).toggleClass('question-form');
        });
    });
}
$('.reorder-subsection').on('click', function(){
    var $element = $(this),
    $modal = getModalWithSubSectionQuestions($element);
    removeButtons($modal, ['.add-more', '.btn-group', '.unassign-question']);
    highlightOnHover($modal);
    activateSortable($modal);
    disableInputFields(false)
    $modal.modal('show');
});

function callOnDropSuper($item) {
    $item.removeClass("dragged").removeAttr("style")
    $("body").removeClass("dragging")
}

function reIndexOrderFields($item, container) {
    var $table = $item.parents('table');
    $table.find('tr').each(function(index, element){
        var $hiddenOrderField = $(element).find('input[type=hidden]');
        var orderId = $hiddenOrderField.val().split(",")[0];
        $hiddenOrderField.val('');
        $hiddenOrderField.val(orderId +","+ index);
    });
}

function activateSortable($modal){
    $modal.find('table').each(function(){
        $(this).sortable({
            containerSelector: 'table',
            itemPath: '> tbody',
            itemSelector: '.sortable-tr',
            placeholder: '<tr class="placeholder"/>',
            onDrop :function ($item, container, _super) {
                callOnDropSuper($item);
                reIndexOrderFields($item, container);
             }
        });
    })
}

