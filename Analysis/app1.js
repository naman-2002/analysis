$(document).ready(function() {
    $('#uploadForm').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#status').text(response.message);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});
