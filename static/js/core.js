$(function(){
	$('form input').each(function(){
		 $(this).focus(function(){
			$(this).removeClass("inactive").removeClass("active");       
		   if($(this).val() == $(this).attr("alt")){
	            $(this).val("");
				$(this).addClass("active");
	        }else{
				$(this).addClass("active");
	        }
	    });
	    $(this).blur(function(){
	        if($(this).val() == $(this).attr("alt") || !$(this).val().length){
				$(this).removeClass("inactive").removeClass("active");
				$(this).addClass("inactive");
	            $(this).val($(this).attr("alt"));
	        }
	    });
	    $(this).blur();
	});
	
	$('#source').click(function(){
		 if($('#source_url').val() != $('#source_url').attr("alt")){
			$(this).focus().select();
		 }	
	})
	
	$('#results').click(function(){
		$(this).focus().select();
	});
	
	$('form').submit(function(){
		$('form input').each(function(){
			if($(this).val() == $(this).attr("alt")){
				$(this).val("");
			}
		});
		return true;
	})
	
	$('.loadexample').click(function(){
		$('#source').val($('.example').val());
	});
	
});


