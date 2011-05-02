/*
var TabSwitch = new Class({
    initialize: function() {
        this.switchers = $$('#tabBox ul li a');
        this.switchers.addClass('off'); //turn off all tab switchers
        this.switchers[0].removeClass('off').addClass('on'); // turn on the first one
        this.sections = $$('#tabBox div.panelSet div.panel');
        this.sections.addClass('hidden');
        this.sections[0].removeClass('hidden').addClass('visible');
        this.sw_sec = this.sections.associate(this.switchers);
        //this.switchers[0].fireEvent('click', []);
                
        this.switchers.addEvent('click', this.switch_tab.bind(this));
    },
    
    switch_tab: function(e) {
        var target = e.target;
        //console.log(target);
        var index = this.switchers.indexOf(target);
        this.switchers.addClass('off');
        target.addClass('on');
        if (target.hasClass('off')) {
            target.removeClass('off');
        };
        this.sections.addClass('hidden');
        this.sections[index].removeClass('hidden').addClass('visible');
        //this.sw_sec[target].removeClass('hidden').addClass('visible');
    },
});
*/
document.addEvent('domready', function() {
    var TS =  new TabSwapper({
        selectedClass: 'on',
        deselectedClass: 'off',
        tabs: $$('#tabBox .tabSet li'),
        clickers: $$('#tabBox .tabSet li span'),
        sections: $$('div.panelSet div.panel'),
        cookieName: 'tabSet',
        smooth: true,
        smoothSize: true,
    });
});
/*
document.addEvent('domready', function() {
    //var BlocksUpDown = new Fx.Morph('dropdown1', {duration: 600, transition: Fx.Transitions.Sine.easeOut});
    $each($$('a[id^=switch_panel_]'), function(el, ind) {
        el.addEvents({
            mouseover: function() {
                new_ind = ind + 1;
                id = 'blocks_panel_' + new_ind;
                $(id).setStyle('background', 'green');
                var BlocksUp = new Fx.Morph(id, {duration: 300, transition: Fx.Transitions.Sine.easeOut});
                BlocksUp.start({
                    height: [10, 50],
                });
            },
            mouseout: function() {
                new_ind = ind + 1;
                id = 'blocks_panel_' + new_ind;
                $(id).setStyle('background', 'red');
                var BlocksDown = new Fx.Morph(id, {duration: 300, transition: Fx.Transitions.Sine.easeOut});
                BlocksDown.start({
                    height: [30, 10],
                });
            },
        });                
    });
});
*/