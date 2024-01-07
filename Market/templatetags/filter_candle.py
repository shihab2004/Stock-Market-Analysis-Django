from django.template import Library

register = Library()


@register.filter()
def get_percent(candle):
    return candle['%']

@register.filter()
def get_candle_dir(candle):
    return candle['dir']


@register.filter()
def get_analysis(candle):
    return candle['html']
