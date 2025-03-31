from django.db import models
from django.forms.models import model_to_dict
from typing import List

def get_hs_fields(model: models.Model) -> List[str]:
    """
    Returns the hs_fields attribute of a django `Model`'s `Meta` class.

    If hs_fields is not defined all editable fields are returned.
    """
    meta = getattr(model, '_meta', None)
    if not meta:
        raise TypeError(f'{model} is not a valid Django model')
    hs_fields = getattr(model, 'hs_fields', [])
    if not hs_fields:
        hs_fields = [field.name for field in meta.get_fields() if field.editable]
    return hs_fields
    
def hs_serialize(data):
    """
    Serializes a Django `QuerySet` or `Model` instance into a `dict` based on the hs_fields attribute defined in the `Model`'s `Meta` class.

    If the passed data does not match either of the previous types, it will be returned as is.
    """
    if isinstance(data, models.query.QuerySet):
        model = data.model
        fields = get_hs_fields(model)
        data = [model_to_dict(instance, fields) for instance in data]
    elif isinstance(data, models.Model):
        model = data.__class__
        fields = get_hs_fields(model)
        data = model_to_dict(data, fields)
    elif isinstance(data, dict):
        return {key: hs_serialize(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [hs_serialize(item) for item in data]
    return data