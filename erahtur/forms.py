# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from village.models import UserProfile
from django.forms.extras.widgets import SelectDateWidget
import datetime
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)
    email = forms.EmailField()
    
    def login_valid(self):
        login = self.cleaned_data['username']
        try:
            db_user = User.objects.get(username=login);
            unique = False
        except User.DoesNotExist:
            unique = True
        valid = bool(re.match(r'^[\w_-]+$', login)) and unique
        if not valid:
            error_message = u'Неправильно введен или занят логин'
            self._errors['username'] = self.error_class([error_message])
        return valid
            
    
class UserProfileForm(ModelForm):
    day_choices = [(d, d) for d in range(1, 32)]
    day_choices.insert(0, (None, u'День'))
    
    month_choices = [(d, d) for d in range(1, 13)]
    month_choices.insert(0, (None, u'Месяц'))

    year_choices = [(d, d) for d in range(1920, 2005)]
    year_choices.reverse()
    year_choices.insert(0, (None, u'Год'))
    
    year = forms.ChoiceField(choices = tuple(year_choices))
    month = forms.ChoiceField(choices = tuple(month_choices))
    day = forms.ChoiceField(choices = tuple(day_choices))

    class Meta:
        model=UserProfile
        fields = ('last_name', 'first_name', 'patronymic', 'icq', 'location', 'avatar', 'phones',)