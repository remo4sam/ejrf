$(document).ready(function(){
    $("input[type=checkbox][name=regions]").on('click', function(){
        var regions = []
        $("input[type=checkbox][name=regions]:checked").each(function(){
                regions.push($(this).val());
            });

        getCountriesFor(regions, function(data){
            $('#extract-countries').html('');
            for(var index=0; index<data.length; index++){
                $('#extract-countries').append("<li class='countries-extract'>"+
                    '<input type="checkbox" name="countries" value="'+ data[index].id +'" id="'+ data[index].name+'"/>'+
                            '<label for="'+data[index].name+'">'+data[index].name+'</label></li>');
            }
        });
    });
});

function getCountriesFor(regions, callback){
    url = "/locations/countries/",
    data = $.param({'regions': regions}, true);
    $.get(url, data, callback);
}