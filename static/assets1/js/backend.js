$('#submitBtn').on('click', function(event) {
    event.preventDefault();
    const formData1 = $('#form1').serializeArray();
    const formData2 = $('#form2').serializeArray();
    // var ill = $('#form2')('input[name=demo-ill]:checked').map(function() {
    //     return this.value;
    // }).get();

    // var all = $('input[name=demo-all]:checked').map(function() {
    //     return this.value;
    // }).get();

    // var illness = ill.join(',');
    // var allergen = all.join(',');

    // const mergedFormData = formData1.concat({'illness': illness}).concat({'allergen': allergen});
    mergedFormData = formData1.concat(formData2)

    $.ajax({
        url: logUrl,
        type: 'POST',
        data: mergedFormData,
        dataType: 'json',
        traditional: true,
        success: function(response, textStatus, jqXHR) {
            console.log('yesyes')
            if ('redirect_url' in response && response.redirect_url) {
                console.log('302')
                window.location.href = response.redirect_url;
            } else {
                console.log('no 302')
                console.log('Data submitted successfully:', response);
                window.location.href = response.redirect_url;
            }
        },
        error: function(xhr, status, error) {
            console.log('Error details:', xhr.status, xhr.statusText, xhr.responseText);
        }
    });
});

$('#resetBtn').on('click', function() {
    $('#form1')[0].reset();
    $('#form2')[0].reset();
});