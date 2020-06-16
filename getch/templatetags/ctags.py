from django import template
register = template.Library()

@register.filter
def score_unitize(score):
    return round(float(score)/10)
