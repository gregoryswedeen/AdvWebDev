$(function(){
	$('submit').click(function(){
		var address = $('#txtPlaces').val();
		$.ajax({
			url: '/getAddress/',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
