$(document).ready(function() {
    var table = null;
    $('#input_data_form').submit(function (event) {
        event.preventDefault();
        if ($('#input_data_form')[0].checkValidity() === false) {
            event.stopPropagation();
            if (table !== null) {
                table.destroy();
                table = null;
                $("#a_nice_table").empty();
            }
        } else {
            $.getJSON('/_get_table', {
                nrow: $("#nrow").val(),
                ncol: $("#ncol").val()

            }, function(data) {

            $('#plot_content').html(data.html_plot);

            if (table !== null) {
                table.destroy();
                table = null;
                $("#a_nice_table").empty();
            }
            table = $("#a_nice_table").DataTable({
                data: data.my_table,
                columns: data.columns

            });
            });
        return false;
        }
        $('#input_data_form').addClass('was-validated');
    });

});