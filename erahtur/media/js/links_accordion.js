document.addEvent('domready', function() {
    var accordion = new Fx.Accordion($$('.toggler'), $$('$$.element'), {
        opacity: 0,
        onActive: function(toggler) { toggler.setStyles({'color': '#f87676', 'font-family': 'Helvetica'});},
        onBackground: function(toggler) {toggler.setStyles({'color': '#000', 'font-family': 'serif'}); }
    });
});