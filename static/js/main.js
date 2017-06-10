$( document ).ready(function() {
    $("#ajax").on("click", function(){
	$.ajax({
	    url: '/ajax',
            data: {},
            dataType: 'json',
	    success: function(data){
	        $('#plot_div').html(data.div);
    		$('#script_div').html(data.script);
            }
        })
    })
});
