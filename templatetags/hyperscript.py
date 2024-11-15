from django import template
from django.utils.safestring import mark_safe
import json
from django.template.context import RequestContext

register = template.Library()

@register.simple_tag(takes_context=True)
def hs_dump(context, data):
    context = context.dicts[-2] if isinstance(context, RequestContext) else context
    data_name = 'data'
        
    for key, value in context.items():
        if data == value:
            data_name = key
            
    data = json.dumps(data)
    hyperscript = f"<div _='init set global {data_name} to {data} then remove me end'></div>"
    return mark_safe(hyperscript)