from django import template
from django.utils.safestring import mark_safe
import json
from django.template.context import RequestContext

register = template.Library()

@register.simple_tag()
def hs_dump(data, name='data'):
    data = json.dumps(data)
    hyperscript = f"<div _='init set global {name} to {data} end'></div>"
    return mark_safe(hyperscript)