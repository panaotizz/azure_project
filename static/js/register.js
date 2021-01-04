$( window ).on( "load", function() {
    console.log( "window loaded" );
});

$(document).on('click','.btn-add', function(){
    var tbody=$(this).closest('tbody');
    var currentEntry=$(this).closest('tr');
    var row=[];
    currentEntry.find('td').each(function (){
        row.push(this.innerHTML);
    });
    tbody.append('<tr>');
    for(var i=0; i<row.length; i++) {
        $(this).closest('tbody').find('tr:last').append('<td>' + row[i] + '</td>');
    }
    tbody.append('</tr>');
    $(this).closest('tbody').find('tr:last input').val();


    currentEntry.find('td:last button').removeClass('btn-add').addClass('btn-rmv');
    currentEntry.find('td:last button i').removeClass('fa-plus').addClass('fa-minus');
});


$(document).on('click','.btn-rmv', function() {
    $(this).closest('tr').remove();
});

// function to extract and submit table data.
function submit(btn) {
    var dataa=[];
    $(' table tbody').find('tr input').each(function (){
        dataa.push($(this).val());
    })
    console.log(dataa,$(btn).data('action'), $(btn).data('csrf'));
jsonData= JSON.stringify(Object.assign({}, dataa));
		console.log(jsonData);
    // json={}
    // json['json']=dataa;

    $.ajax({
        type: 'POST',
        url: $(btn).data('action'),
        data: {
            'json' : jsonData,
            'csrfmiddlewaretoken': $(btn).data('csrf'),
        } ,
        success: function (data) {
            console.log(data);
        }
    });


}