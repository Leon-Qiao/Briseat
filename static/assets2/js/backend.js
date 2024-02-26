$(document).ready(function() {
    $('#photoLink').on('click', function(event) {
        event.preventDefault(); 
        $('#photoFile').trigger('click');
    });
});

$('#photoFile').on('change', function() {
    var file = this.files[0];
    var formData = new FormData();
    formData.append('image', file);
    $.ajax({
        url: imgUrl,
        type: 'POST',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: formData,
        contentType: false, 
        processData: false,
        
        success: function(response, textStatus, jqXHR) {
            if ('redirect_url' in response && response.redirect_url) {
                window.location.href = response.redirect_url;
            } else {
                console.log('Data submitted successfully:', response);
                window.location.href = response.redirect_url;
            }
        },
        error: function(xhr, status, error) {
            console.log('Error details:', xhr.status, xhr.statusText, xhr.responseText);
        }
    });
});
