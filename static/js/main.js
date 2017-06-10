$( document ).ready(function() {
    $("#ajax").on("click", function(){
	$.ajax({
	    type: "POST",
	    url: '/ajax',
	    success: function(data){
	        $('#plot_div').html(data.div);
    		$('#script_div').html(data.script);
            },
	    error: function(error){
		console.log(error);
	    }
        })
    })

    // Stream
    $("#stream").on("click", function(){
	$.ajax({
	    type: "POST",
	    url: '/stream',
	    success: function(data){
	        $('#stream_plot').html(data.div);
    		$('#stream_script').html(data.script);
            },
	    error: function(error){
		console.log(error);
	    }
        })
    })
});
