$(document).on('click', '#hide-assigned-questions', function() {
    var hideQuestions = "";
    if($(this).is(':checked')){
        hideQuestions = "?hide=1";
    }

    var subsection_id = $(this).attr('subsection-id'),
        assign_to_subsection_url = "/subsection/" + subsection_id +"/assign_questions/"+hideQuestions;
    $.get(assign_to_subsection_url, function( data ) {
        var $holder = $('<div></div>').append(String(data));
        var content =  $holder.find("#question-list").html()
        $( "#assign-question-ajax-content-"+subsection_id ).html(content);

        if(hideQuestions){
            $("#hide-assigned-questions").attr('checked', true);
        }
    });
});



