from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

def _snake_case_to_camel_case(data: str):
    words = data.split('_')
    return f'{words[0]}{''.join([word.capitalize() for word in words[1:]])}'

def _dict_to_camel_case(data: dict):
    if isinstance(data, dict):
        return {_snake_case_to_camel_case(key): _dict_to_camel_case(value) for key, value in data.items()}
    else:
        return data

def _construct_hyperscript(data, name=None, accepted_kwargs: dict={}, **kwargs):
    DEFAULT_KWARGS = {'show': bool, 'translate': bool, 'scope': str, 'wrap': bool}
    accepted_kwargs = {**DEFAULT_KWARGS, **accepted_kwargs}
    for key, value in kwargs.items():
        if key not in accepted_kwargs:
            raise TypeError(f'Unexpected keyword argument: {key}. Accepted arguments: {', '.join([f'{kwarg}: {type.__name__}' for kwarg, type in accepted_kwargs.items()])}.')
        expected_type = accepted_kwargs[key]
        if not isinstance(value, expected_type):
            raise TypeError(f'Invalid type for keyword argument {key}: expected {expected_type}, got {type(value).__name__}')
    
    scope = kwargs.get('scope', 'global')
    wrap = kwargs.get('wrap', True)

    if kwargs.get('translate', True):
        data = _dict_to_camel_case(data)

    if kwargs.get('expand', False):
        if not isinstance(data, dict):
            raise TypeError(f'Invalid type for mapping: expected dict, got {type(data).__name__}')
        assignment = ' '.join([f'set {scope} {key} to {json.dumps(value)}' for key, value in data.items()])
    else:
        assignment = f'set {scope} {name} to {json.dumps(data)}'

    hyperscript = f'init {assignment}'

    if not kwargs.get('show', False):
        if not wrap:
            hyperscript = f'{hyperscript} then remove @_ from me'
        else:
            hyperscript = f'{hyperscript} then remove me'

    hyperscript = f'{hyperscript} end'

    if wrap:
        hyperscript = f"<div _='{hyperscript}'></div>"

    return mark_safe(hyperscript)

@register.simple_tag()
def hs_dump(data, name: str, **kwargs):
    return _construct_hyperscript(data, name, **kwargs)

@register.simple_tag()
def hs_expand(data, **kwargs):
    kwargs['expand'] = True
    accepted_kwargs = {'expand': bool}
    return _construct_hyperscript(data, accepted_kwargs=accepted_kwargs, **kwargs)