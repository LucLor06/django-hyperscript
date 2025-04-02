<img src="https://github.com/LucLor06/django-hyperscript/blob/main/django-hyperscript.png?raw=true" width=200>

# Django hyperscript

**Django Hyperscript** is a simple Django template tag library for dumping data into [_hyperscript](https://github.com/bigskysoftware/_hyperscript).  
It’s a wrapper around [hyperscript-dump](https://github.com/LucLor06/hyperscript-dump), with Django-specific features like automatic model serialization and safe output for templates.

---
## Installation

1. Install using pip:
```bash
pip install django-hyperscript
```

2. Add `django_hyperscript` to `INSTALLED_APPS` in your Django project's `settings.py`:
```python
# settings.py

INSTALLED_APPS = [
    ...,
    'django_hyperscript',
]
```

3. Load the tag library in the necessary templates:
```django
{% load hyperscript %}
```

---
## Usage

By default, django-hyperscript wraps its output in a `<div>` with a class of `hs-wrapper`.

### `hs_dump`

Dumps data into a single hyperscript variable.
```django
{% hs_dump data 'myData' %}
```
assuming `data` is `{"foo": "bar"}`, the tag would output
```html
<div class="hs-wrapper" _="
init
    set global myData to {'foo': 'bar'} 
    then remove me 
end"></div>
```

Using the kwarg `flatten` will assign the first layer of a dictionary's key value pairs into hyperscript variables. The `name` argument is negligible when using `flatten`.
```django
{% hs_dump data flatten=True %}
```
assuming `data` is `{"foo": "bar", "baz": "qux"}`, the tag would output
```html
<div class="hs-wrapper" _="
init
    set global foo to 'bar'
    set global baz to 'qux' 
    then remove me 
end"></div>
```

---
## Model Serialization

Django-hyperscript includes a built-in lightweight serializer to help convert Django `Model` instances and `QuerySet`s into plain data structures for use in templates. This includes instances or querysets that are nested within dictionaries or lists, which will be serialized recursively.

By default, the serializer returns all editable fields defined on the model. However, you can customize this by adding an `hs_fields` attribute to your model, which is a list of field names you want exposed.

```python
class Book(models.Model):
    name = models.CharField(max_length=32)
    year_published = models.SmallIntegerField()

    hs_fields = ['name', 'year_published']
```

would return an instance as

```json
{
   "name": "foo",
   "year_published": 1986
}
```

This serializer is intentionally minimal and does not support advanced features like relation traversal, nested serialization, field aliasing, or custom computed fields. If you need those capabilities, consider serializing your data ahead of time using Django REST Framework, or a custom serializer.

If needed, this serializer can be accessed via
```python
from django_hyperscript.serializer import hs_serialize
```
---
## Configuration

`hs_dump` supports all kwargs from [hyperscript-dump](https://github.com/LucLor06/hyperscript-dump)'s `build_hyperscript` along with some additional ones:

### `preserve`
*Type*: `bool` | *Default*: `False`

Keeps the element the hyperscript is on in the DOM after initializing if `True`.

### `camelize`
*Type*: `bool` | *Default*: `True`

"Camelizes" dictionary keys from snake case (snake_case) to camel case (camelCase) to fit JavaScript naming conventions.

### `flatten`
*Type*: `bool` | *Default*: `False`

If `True`, each key value pair in a dictionary is assigned as a separate variable, rather than as a single object.

**Note:** Requires data to be a dictionary.

### `scope`
*Type*: `str` | *Default*: `global`

Determines the scope of the hyperscript variable (global, element, or local).

### `event`
*Type*: `str, None` | *Default*: `init`

Specifies the event that triggers assignment. The hyperscript "on" keyword should not need be provided. When set to none only the hyperscript assignment statements will be returned.

**Note:** If **`preserve`** is `False` (which it is by default), the element will not be removed until after the event is fired and values are set.

### `debug`
*Type*: `bool` | *Default*: `False`

Logs the set variable name(s) and value(s).

### `wrap`
*Type*: `bool` | *Default*: `True`

Wraps the hyperscript in a `<div>` with its `display` set to `none` if `True`, otherwise returns the raw hyperscript text.

### `class`
*Type*: `str` | *Default*: `hs-wrapper`

Sets the HTML class/classes on the wrapper `<div>`.

## Final example
```django
{% hs_dump data 'my_data' preserve=True camelize=False scope='element' wrap=False %}
```
assuming `data` is `{"my_value": 25}`, the tag would output
```python
"init set element my_data to {'my_value': 25} end"
```
In this example:
- The hyperscript remains in the DOM since **`preserve`** is `True`
- The keys within the dumped data remain in snake case since **`camelize`** is `False`
- The variable is scoped to the element the hyperscript belongs to since **`scope`** is set to `'element'`
- The output is just the raw hyperscript text since **`wrap`** is set to `False`

---
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
