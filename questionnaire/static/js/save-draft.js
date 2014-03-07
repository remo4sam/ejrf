
$(document).ready(function() {
    warnBeforeNavigatingAway();

});

$( "#questionnaire_entry :input" ).change(function() {
  form_has_changed = true;
});

$("#questionnaire_entry").on('submit', function(){
    form_has_changed = false;
    this.submit();
});

function warnBeforeNavigatingAway(){
    saveDraftOnTabNavigation();
    window.onbeforeunload = function(){
      if(form_has_changed){
        return "Are you sure you want to navigate away from this page?\nAll unsaved changes will be lost.";
       }
   };
}

function saveDraftOnTabNavigation(){
    $('.section_tab ').click(function(e){
       e.preventDefault()
       var url = $(this).attr('href');
       if($("#preview").val() == 1){
           window.location = url;
       }
       else if (form_has_changed){
            $('#redirect_url').val(url);
            $('#questionnaire_entry').submit();
       }else
            window.location = url;
    });

    $('#preview-questionnaire').click(function(e){
       e.preventDefault()
       var url = $(this).attr('href');

       if (form_has_changed){
            $('#redirect_url').val(url);
            $('#questionnaire_entry').submit();
       }else
            window.location = url;
    });
}