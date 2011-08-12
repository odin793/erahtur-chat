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
    
    /* block of publication's content via ajax is injected to the page */
    $$('.read').each(function(el, ind) {
        el.addEvent('click', function(e) {
            e.stop();
            var pub_id = e.target.getProperty('id').split('-')[1];
            link_element = $(e.target.getProperty('id')) // we will inject news block after this element            
            if (link_element.getProperty('class') != 'read-down') { // if user didn't clicked on arrow yet or clicked twice
                new Request({
                    url: '/ajax_news_block/',
                
                    onSuccess: function(r) {                    
                        var ajax_news_block = new Element('p', { // create new p for publication text
                            styles: {
                                opacity: '0',
                            },
                            id: 'ajax_news_block-' + pub_id,
                        });
                    
                        // create inner html for news block                 
                        ajax_news_block.set('html', r);
                        ajax_news_block.inject(link_element, 'after');
                    
                        /* change arrow type and it's class */
                        link_element.set('html', '&darr;');
                        link_element.setProperty('class', 'read-down');
                    
                        var appearance_Fx = new Fx.Morph(ajax_news_block, {duration: 400,});
                        appearance_Fx.start({
                            'opacity': [0, 1],
                        });
                    },                
                }).post({pub_id: pub_id});
            }
            
            else { // arrow is already in down position and user clicked once again
                $('ajax_news_block-' + pub_id).empty(); // delete ajax_news_block
                /* change arrow type and it's class back to initial values */
                link_element.set('html', '&rarr;');
                link_element.setProperty('class', 'read');
            };            
        });
    });
    
    if ( $('hidden_chat_form') == undefined ) { /* if user is not logged in */
        chat_link = $('go_to_chat');
        chat_notification_block = $('chat_notification_block');
        chat_notification_block.addEvent('burn', function(text) {
            chat_notification_block.set('html', text);
            fx.start({
                'background-color': ['#e9a936', '#fff'],
                'opacity': [1,0],
                'visibility': 'visible',
            });
        });
        var fx = new Fx.Morph('chat_notification_block', {
            duration: 7500,
            wait: false,
            transition: Fx.Transitions.linear.easeOut
        });
        
        chat_link.addEvent('click', function(e) {
            e.stop();
            chat_notification_block.fireEvent(
                'burn', 
                'Пожалуйста, <a href="/login_page" class="notification">войдите</a> или <a href="/accounts/registration/" class="notification">зарегистрируйтесь.</a>'
            );
        });
    };
    
});