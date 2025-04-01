from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe, SafeString
from ..serializer import hs_serialize
from hyperscript_dump import build_hyperscript
from typing import Any

register = template.Library()

@register.simple_tag()
def hs_dump(
    data: Any,
    name: str = "data",
    *,
    wrap: bool = True,
    classes: str = "hs-wrapper",
    **kwargs
) -> SafeString:
    """
    Injects Python data into Hyperscript via a Django template tag.

    This tag serializes Django data (such as model instances, querysets, or native types),
    passes it to the `build_hyperscript()` utility from `hyperscript-dump`, and optionally wraps
    the output in a <div> element.

    By default, the generated Hyperscript block is wrapped in a <div> with a class of
    "hs-wrapper" and a Hyperscript `_=` attribute.

    Args:
        data (Any): The data to be serialized and assigned to a Hyperscript variable.
        name (str): The name of the variable to assign. Defaults to "data".
        wrap (bool): If True, wraps the Hyperscript output in a <div>. Defaults to False.
        classes (str): HTML class for the wrapper element (if wrap=True). Defaults to "hs-wrapper".
        **kwargs: Optional keyword arguments forwarded to `build_hyperscript()`, such as:
            - preserve (bool): Prevent removal of the element after assignment.
            - flatten (bool): Assign each key/value in a dict as its own variable.
            - camelize (bool): Convert snake_case keys to camelCase.
            - debug (bool): Add console logging of assigned values.
            - scope (str): Hyperscript variable scope (e.g., "global", "local").
            - event (str): Event that triggers assignment.

    Returns:
        SafeString: A safe, rendered block of Hyperscript code (wrapped in a <div> unless wrap=False).
    """
    classes = conditional_escape(classes)

    data = hs_serialize(data)
    hyperscript = build_hyperscript(data, name, **kwargs)

    if wrap:
        hyperscript = f"<div class='{classes}' _='{hyperscript}'></div>"

    return mark_safe(hyperscript)