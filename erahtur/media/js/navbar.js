/*
document.addEvent('domready', function() {
    var navbar_links = $('navbar').getElements('a[class^=nb]');
    //var mySlide = new Fx.Morph('dropdown1', {duration: 600, transition: Fx.Transitions.Sine.easeOut});
    //var mySlidein = new Fx.Morph('dropdown1', {duration: 300, transition: Fx.Transitions.Sine.easeOut});
    navbar_links.addEvent('mouseover', function(e){
        e.target.highlight('#FF2800', '#f87676');
    });
});
*/

document.addEvent('domready', function() {
    
    /* footer is on center of the window */
    
    var x = Math.round((document.body.clientWidth-1000) / 2);
    $('footer').setStyle('left', x + 'px');

    /* hightlights link in the navigation bar for the current url */
    var pages = ['publications', 'history', 'organizations', 'neighbours', 'communications', 'creation', 'links'];
    current_location = window.location.pathname;
    pages.each(function(item, index) {
        if (current_location.contains(item)) {
            link_id = 'nb_' + item;
            $(link_id).getParent().addClass('active_tab');
            $(link_id).addClass('active_link');
        };
    });
    var news_pages = ['district', 'region', 'oblast'];
    news_pages.each(function(item, index) {
        if (current_location.contains(item)) {
            link_id = 'pub_' + item;
            $(link_id).getParent().addClass('active_tab');
            $(link_id).addClass('active_link');
        };
    });
    
    /* photos effect */
    
    if ($$('.photo_thumb') != undefined) {
        $$('.photo_thumb').each(function(el, ind) {
            el.addEvents({
                mouseover: function() {
                    el.setStyle('opacity', '1');
                },
                mouseout: function() {
                    el.setStyle('opacity', '0.9');
                },
            });
        });
    };
    
    /* hidden chat form */
    
    $('go_to_chat').addEvent('click', function(e) {
        e.stop();
        if ($('hidden_chat_form') != undefined) {
            $('hidden_chat_form').submit();
        }
    });
    
    /* window is resized. footer is still on center of the window */
    window.addEvent('resize', function() {
       x = Math.round((document.body.clientWidth-1000) / 2);
       $('footer').setStyle('left', x + 'px')
    });
    
});
