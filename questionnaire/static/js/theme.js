$('#new-themes-modal-form,form[id^=edit-theme]').each(function(){
    $(this).validate({rules: { 'name': 'required'}});
})
