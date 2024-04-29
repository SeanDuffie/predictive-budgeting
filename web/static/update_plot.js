// https://stackoverflow.com/questions/50297490/update-a-bokeh-plot-using-ajax
$(document).ready(function(){
    $('#calculate').on('click', function(e){
        // prevent page being reset, we are going to update only
        // one part of the page.
        e.preventDefault()
        $.ajax({
        url:'./_get_table',
        type:'post',
        data:{'nrow':$("#nrow").val(),
                'ncol':$("#ncol").val()},
        success : function(data){
            // server returns rendered "update_content.html"
            // which is just pure html, use this to replace the existing
            // html within the "plot content" div
            $('#plot-content').html(data)
        }
        })
    });
});