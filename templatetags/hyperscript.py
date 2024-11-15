from django import template
from django.utils.safestring import mark_safe
import json
from django.template.context import RequestContext

register = template.Library()

def _snake_case_to_camel_case(data: str):
    words = data.split('_')
    return f'{words[0]}{''.join([word.capitalize() for word in words[1:]])}'

def _dict_to_camel_case(data: dict):
    if isinstance(data, dict):
        return {_snake_case_to_camel_case(key): _dict_to_camel_case(value) for key, value in data.items()}
    else:
        return data

@register.simple_tag()
def hs_dump(data, name='data', **kwargs):
    ACCEPTED_KWARGS = {'show': bool, 'translate': bool}
    
    for key, value in kwargs.items():
        if key not in ACCEPTED_KWARGS:
            raise TypeError(f'Unexpected keyword argument: {key}. Accepted arguments: {', '.join([f'{kwarg}: {type.__name__}' for kwarg, type in ACCEPTED_KWARGS.items()])}.')
        
        expected_type = ACCEPTED_KWARGS[key]
        if not isinstance(value, expected_type):
            raise TypeError(f'Invalid type for keyword argument {key}: expected {expected_type}, got {str(type(value))}')

    if kwargs.get('translate', True):
        data = _dict_to_camel_case(data)

    data = json.dumps(data)
    hyperscript = f'init set global {name} to {data}'


    if not kwargs.get('show', False):
        hyperscript = f'{hyperscript} then remove me'
        
    hyperscript = f"<div _='{hyperscript} end'></div>"
    return mark_safe(hyperscript)