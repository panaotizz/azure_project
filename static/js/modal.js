function revoke(btn){
    const filename = $(btn).closest('li').find('a').text();
    $.ajax({
        type: 'POST',
        url: $(btn).closest('li').children('button').data('action'),
        data: {
            'filename': filename,
            'csrfmiddlewaretoken': $(btn).closest('li').children('button').data('csrf')
        },
        success: function (data) {
            $('.div-modal').replaceWith(data.context);
            $('.modal').modal();
        }
    });
}

function remove(btn){
    const filename = $(btn).closest('.modal').find('.modal-title').html();
    const user = $(btn).closest('div').find('li')[0].innerText;
    $.ajax({
        type: 'POST',
        url: $(btn).data('action'),
        data: {
            'filename': filename,
            'user': user,
            'csrfmiddlewaretoken': $(btn).data('csrf')
        },
        success: function () {
            $('.modal').modal('toggle');
        }
    });
}

function save(btn){
    const filename = $(btn).closest('.modal').find('.modal-title').html();
    const user = $(btn).closest('.modal').find('.input-new-revoke').val();
    $.ajax({
        type: 'POST',
        url: $(btn).data('action'),
        data: {
            'filename': filename,
            'user': user,
            'csrfmiddlewaretoken': $(btn).data('csrf')
        },
        success: function () {
            $('.modal').modal('toggle');
        }
    });
}