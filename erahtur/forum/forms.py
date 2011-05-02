# _*_ coding: utf-8 _*_

from django import forms
from django.utils.translation import ugettext as _

class CreateThreadForm(forms.Form):
    title = forms.CharField(label=u'Название темы', max_length=100)
    body = forms.CharField(label=u'Текст сообщения', widget=forms.Textarea(attrs={'rows':8, 'cols':100}))
    #subscribe = forms.BooleanField(label=u"Подписаться через email", required=False)

class ReplyForm(forms.Form):
    body = forms.CharField(label=u'Текст сообщения', widget=forms.Textarea(attrs={'rows':8, 'cols':100}))
    #subscribe = forms.BooleanField(label=u"Подписаться через email", required=False)

