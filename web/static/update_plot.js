// https://stackoverflow.com/questions/50297490/update-a-bokeh-plot-using-ajax
$(document).ready(function(){
    $('#sav_submit').on('click', function(e){
        // prevent page being reset, we are going to update only
        // one part of the page.
        e.preventDefault()
        $.ajax({
            url:'./form_savings/',
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

$(document).ready(function(){
    $('#inv_submit').on('click', function(e){
        // prevent page being reset, we are going to update only
        // one part of the page.
        e.preventDefault()
        $.ajax({
        url:'./form_investment/',
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

$(document).ready(function(){
    $('#ast_submit').on('click', function(e){
        // prevent page being reset, we are going to update only
        // one part of the page.
        e.preventDefault()
        $.ajax({
        url:'./form_asset/',
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

$(document).ready(function(){
    $('#loan_submit').on('click', function(e){
        // prevent page being reset, we are going to update only
        // one part of the page.
        e.preventDefault()
        $.ajax({
        url:'./form_loan/',
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