from django import template
from django.utils.safestring import mark_safe
import json
from django.template.context import RequestContext

register = template.Library()

@register.simple_tag()
def hs_dump(data, name='data', **kwargs):
    ACCEPTED_KWARGS = {'show': bool}
    
    for key, value in kwargs.items():
        if key not in ACCEPTED_KWARGS:
            raise TypeError(f'Unexpected keyword argument: {key}. Accepted arguments: {', '.join([f'{kwarg}: {type.__name__}' for kwarg, type in ACCEPTED_KWARGS.items()])}.')
        
        expected_type = ACCEPTED_KWARGS[key]
        if not isinstance(value, expected_type):
            raise TypeError(f'Invalid type for keyword argument {key}: expected {expected_type}, got {str(type(value))}')

    data = json.dumps(data)
    hyperscript = f'init set global {name} to {data}'

    if not kwargs.get('show', False):
        hyperscript = f'{hyperscript} then remove me'
        
    hyperscript = f"<div _='{hyperscript} end'></div>"
    return mark_safe(hyperscript)