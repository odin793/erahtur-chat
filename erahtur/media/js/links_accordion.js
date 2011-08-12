document.addEvent('domready', function() {
    var accordion = new Fx.Accordion($$('.toggler'), $$('$$.element'), {
        opacity: 0,
        //onActive: function(toggler) { toggler.setStyles({'color': '#f87676', 'font-family': 'Helvetica'});},
        onActive: function(toggler) { toggler.addClass('active_font')},
        /*onBackground: function(toggler) {toggler.setStyles({'color': '#000', 'font-family': 'serif'}); }*/
        onBackground: function(toggler) {toggler.removeClass('active_font') },
    });
});