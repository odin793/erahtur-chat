from django import template
import pytils

register = template.Library()

@register.filter(name='pytils_date')
def pytils_date(date):
    return pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=date)