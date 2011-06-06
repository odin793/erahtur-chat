document.addEvent('domready', function() {
	
	/*comment button is enabled or disabled*/
	
	if ($('comment_body') != undefined) {
    	$('comment_body').addEvent('keyup', function(e) {
        	if ($('comment_body').value != '') {
        		$('add_comment_button').removeProperty('disabled');
        	}
        	else {
        		$('add_comment_button').setProperty('disabled', 'disabled');
        		$('comment_body').value = '';
        	}
        });    
    };   
});
