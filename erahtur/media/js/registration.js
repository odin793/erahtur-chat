var FieldManager = new Class({
    
    mark_mistake: function(field) {
        field.setStyle('background', '#FE3F44');
    },
    
    unmark_mistake: function(field) {
        field.setStyle('background', 'white');
    },
    
    clear_field: function(field) {
        field.setProperty('value', '');
    },
    
});

var RegistrationManager = new Class({
    Implements: FieldManager,
    
    initialize: function() {
        this.reg_form = $('reg_form');
        this.username = this.reg_form.username;
        this.password1 = this.reg_form.password1;
        this.password2 = this.reg_form.password2;
        this.email = this.reg_form.email;
        this.username_valid = true;
        this.password_valid = true;
        this.email_valid = true;
        this.username_unique = true;
        
        this.reg_form.addEvent('submit', this.form_check.bind(this));
        this.reg_form.getElement('#check_username_unique').addEvent('click', this.is_username_unique.bind(this));
        //this.reg_form.username.addEvent('blur', this.is_username_unique.bind(this));
    },
    
    form_check: function(e) {
        e.stop();
        this.username_check();
        this.password_check();
        this.email_check();
        if (this.username_valid & this.password_valid & this.email_valid & this.username_unique) {
            this.reg_form.submit();
        }
    },
    
    username_check: function() {
        var username = this.username.getProperty('value').trim()
        var re = /\s/;
        if (username.test(re) | username == '') {
            this.mark_mistake(this.username);
            this.username_valid = false;
        }
        else {
            this.unmark_mistake(this.username);
            this.username_valid = true;
        };
    },
    
    is_username_unique: function(e) {
        e.stop();
        this.username_check();
        if (this.username_valid) {
            new Request({
                url: '/accounts/is_username_unique/',
                onSuccess: function(r) {
                    //username_status.setProperty('html', r);
                    if (r=='good') {
                        this.username.setStyle('background', 'green');
                        this.username_unique = true;
                    }
                    else {
                        this.mark_mistake(this.username);
                        this.username.setProperty('value', 'уже занят');
                        this.username_unique = false;
                    }
                }.bind(this),
                onFailure: function(r) {
                    //username_status.setProperty('html', r.responseText);
                    this.mark_mistake(this.username);
                    this.username_unique = false;
                },
            }).post({username: this.username.getProperty('value').trim()});            
        }
        else {
            //username_status.setProperty('html', 'исправьте ошибку');
            this.mark_mistake(this.username);
            this.username_unique = false;
        };
    },
    
    password_check: function() {
        var password1 = this.password1.getProperty('value').trim();
        var password2 = this.password2.getProperty('value').trim();
        if (password1 != password2 & password1 != '') {
            this.mark_mistake(this.password2);
            this.unmark_mistake(this.password1);
            this.clear_field(this.password2);
            this.password_valid = false;
        }
        else if (password1 != password2 & password1 == '') {
            this.mark_mistake(this.password1);
            this.unmark_mistake(this.password2);
            this.password_valid = false;        
        }    
        else if (password1 == '' & password2 == '') {
            this.mark_mistake(this.password1);
            this.mark_mistake(this.password2);
            this.password_valid = false;
        }
        else if (password2 == '') {
            this.mark_mistake(this.password2);
            this.password_valid = false;
        }
        else if (password1 == '') {
            this.mark_mistake(this.password1);
            this.password_valid = false;
        }
        else {
            this.unmark_mistake(this.password1);
            this.unmark_mistake(this.password2);
            this.password_valid = true;
        };
    },
    
    email_check: function() {
        var r = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if (!this.email.getProperty('value').trim().test(r)) {
            this.mark_mistake(this.email);
            this.email_valid = false;
        }
        else {
            this.unmark_mistake(this.email);
            this.email_valid = true;
        };
    },
    
});


var UserProfileManager = new Class({
    Implements: FieldManager,
    
    initialize: function() {
        this.profile_form = $('profile_form');
        this.last_phone = $$('.phone').getLast();
        this.add_phone_btn = $$('.add_phone');
        this.last_site = $$('.site').getLast();
        this.add_site_btn = $$('.add_site');
        this.icq = this.profile_form.getElement('#id_icq');
        this.first_name = this.profile_form.getElement('#id_first_name');
        this.last_name = this.profile_form.getElement('#id_last_name');
        this.site = this.profile_form.getElement('#id_site');
        var avatar_defined = $defined($('avatar_image'));
        if (avatar_defined) {
            this.change_avatar_link = this.profile_form.getElement('#change_avatar');
            this.new_avatar = this.profile_form.getElement('#.new_avatar');
            
            this.change_avatar_link.addEvent('click', this.change_avatar.bind(this));
        };
        this.first_name_valid = true;
        this.last_name_valid = true;
        this.phone_valid = true;
        this.icq_valid = true;
        this.site_valid = true;
        
        this.profile_form.addEvent('submit', this.profile_form_check.bind(this));
        this.add_phone_btn.addEvent('click', this.add_phone.bind(this));
        this.add_site_btn.addEvent('click', this.add_site.bind(this));
    },
    
    change_avatar: function(e) {
        e.stop();
        this.new_avatar.setStyle('visibility', 'visible');
    },
    
    profile_form_check: function(e) {
        e.stop();
        this.names_check();
        this.phone_check();
        this.icq_check();
        this.site_check();
        if (this.first_name_valid & this.last_name_valid & this.icq_valid & this.phone_valid & this.site_valid) {
            this.profile_form.submit();
        };
    },
    
    add_phone: function(e) {
        e.stop();
        var i=0;
        $each($$('.phone'), function(el, ind) {
            i += 1; //number of phone fields
        });
        if (i < 10) {
            var phone_wrap = new Element('p', { // create new wrap for input field
                styles: {
                    opacity: '0',
                },
            });
            // create inner html for wrapper
            phone_wrap.set('html', '<input type="text" maxlength="20" name="phone" class="phone">');
            phone_wrap.inject(this.last_phone, 'after');
            var appearance_Fx = new Fx.Morph(phone_wrap, {duration: 400,});
            appearance_Fx.start({
                'opacity': [0, 1],
            });
            this.last_phone = phone_wrap;
        };
    },
    
    add_site: function(e) {
        e.stop();
        var i=0;
        $each($$('.site'), function(el, ind) {
            i += 1; //number of phone fields
        });
        if (i < 10) {
            var site_wrap = new Element('p', { // create new wrap for input field
                styles: {
                    opacity: '0',
                },
            });
            // create inner html for wrapper
            site_wrap.set('html', '<input type="text" maxlength="60" name="site" class="site">');
            site_wrap.inject(this.last_site, 'after');
            var appearance_Fx = new Fx.Morph(site_wrap, {duration: 400,});
            appearance_Fx.start({
                'opacity': [0, 1],
            });
            this.last_site = site_wrap;
        };
    },
    
    names_check: function() {
        if (this.first_name.value.trim() == '') {
            this.mark_mistake(this.first_name);
            this.first_name_valid = false;
        }
        else {
            this.unmark_mistake(this.first_name);
            this.first_name_valid = true;
        };
        
        if (this.last_name.value.trim() == '') {
            this.mark_mistake(this.last_name);
            this.last_name_valid = false;
        }
        else {
            this.unmark_mistake(this.last_name);
            this.last_name_valid = true;
        };        
    },
    
    phone_check: function() {
        var r = /^\+?(\s{0,2}\d+\s{0,2}\-{0,2}\s{0,2})*$/;    
        var phones_list = $$('.phone');
        var bad_phones_list = phones_list.filter(function(el, ind) {
            return !el.getProperty('value').trim().test(r);
        });
        phones_list.each(function(el, ind) {
            this.unmark_mistake(el); // first, unmark all mistakes
        }.bind(this));
        bad_phones_list.each(function(el, ind) {
            this.mark_mistake(el); // then mark bad fields
        }.bind(this));
        (this.len(bad_phones_list)) ? this.phone_valid = false : this.phone_valid = true;
    },
    
    icq_check: function() {
        //var r = /^\d*$/;    
        var r = /^(\s{0,2}\d+\s{0,2}\-{0,2}\s{0,2})*$/;    
        if (!this.icq.getProperty('value').trim().test(r)) {
            this.mark_mistake(this.icq);
            this.icq_valid = false;                
        }
        else {
            this.icq_valid = true;
            this.unmark_mistake(this.icq);
        };
    },
    
    site_check: function() {
        var r = /^(((ht|f)tp(s?))\:\/\/)?(www.|[a-zA-Z0-9].)[a-zA-Z0-9\-\.]+\.(com|edu|gov|mil|net|org|biz|info|name|museum|us|ca|uk|ru)(\:[0-9]+)*(\/($|[a-zA-Z0-9\.\,\;\?\'\\\+&%\$#\=~_\-]+))*$/;    
        var sites_list = $$('.site');
        var bad_sites_list = sites_list.filter(function(el, ind) {
            return !el.getProperty('value').trim().test(r) & el.getProperty('value').trim() != '';
        });
        sites_list.each(function(el, ind) {
            this.unmark_mistake(el); // first, unmark all mistakes
        }.bind(this));
        bad_sites_list.each(function(el, ind) {
            this.mark_mistake(el); // then mark bad fields
        }.bind(this));
        (this.len(bad_sites_list)) ? this.site_valid = false : this.site_valid = true;
        
    },
    
    len: function(array) {
        var i = 0;
        array.each(function(el, ind) {
            i += 1;
        })
        return i;
    },
    
});

if (window.location.pathname.contains('accounts/registration')) {
    document.addEvent('domready', function() {
        var rm = new RegistrationManager();  
    });    
}; 

if (window.location.pathname.contains('accounts/user_profile_handle')) {
    document.addEvent('domready', function() {
        var upm = new UserProfileManager();  
    });    
};

document.addEvent('domready', function() {
    if ($$('.login_form') != undefined) {
        login_forms = $$('.login_form'); //there can be 2 forms if we are on "/login_page" url
                
        login_forms.each(function(el, ind) {
            login = el.getElement('.login');
            password = el.getElement('.password');

            login.addEvents({
                focus: function(e) {
                    if (e.target.value == 'login') {
                        e.target.value = '';
                    };
                },
                blur: function(e) {
                    if (e.target.value == '') {
                        e.target.value = 'login';
                    };   
                },   

            });
            
            password.addEvents({
                focus: function(e) {
                    e.target.value = '';
                },
                blur: function(e) {
                    if (e.target.value == '') {
                        e.target.value = 'login';
                    };
                },
            });
            
        });    
    };
}); 