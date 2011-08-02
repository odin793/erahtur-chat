# _*_ coding: utf-8 _*_;

from django import template
import pytils

register = template.Library()

@register.filter(name='pytils_date')
def pytils_date(date):
    return pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=date)
    
@register.filter(name='month_name')
def month_name(month):
    months = {
        1: u'Январь', 2: u'Февраль', 3: u'Март', 4: u'Апрель', 
        5: u'Май',6: u'Июнь', 7: u'Июль', 8: u'Август', 
        9: u'Сентябрь', 10: u'Октябрь', 11: u'Ноябрь', 12: u'Декабрь'
    }
    return months[int(month)]
