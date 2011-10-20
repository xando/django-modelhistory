# django-modelhistory
[https://github.com/xando/django-modelhistory](http://github.com/xando/django-modelhistory)


## Description:
Simple model logging helper for django projects. Covers functionality of discovering action taken on object: DELETE, UPDATE, CREATE and creates and saves suitable message to database. Supports simple db.models.Models objects as well as forms, formset and inlineformset based on Django ORM Models 

## Status:
This application is pretty much in alpha stage, so be careful :) 

## How to use it?:

First you have to add modelhistory do your INSTALLED_APPS inside **settings.py**.

```python
INSTALLED_APPS = (
    ...
    'modelhistory'
)
```

Everywhere where you want to use History you have to place this import.

```python
from django_history.models import History
```


### objects
```python
obj = SimpleModel.objects.create(name="So cool name")
History.objects.log_object(obj)
```

### forms (model forms)
```python
form = SimpleModelForm(request.POST)
if form.is_valid():
    form.save()
    history_log = History.objects.log_form(form)
```

### formsets (model formsets)
```python
formset = ModelFormSet(request.POST)
if formset.is_valid():
    formset.save()
    history_log = History.objects.log_formset(formset)
```

### inline formsets (inline model formsets)
```python
obj = SimpleModel.objects.create(name="So cool name")
formset = ModelInlineFormSet(request.POST, instance=obj)
if formset.is_valid():
    formset.save()
    history_log = History.objects.log_inlineformset(formset)
```

## Tests:
Tests are [here](https://github.com/xando/django-modelhistory/modelhistory/tests/). 

```sh
./runtests.py
```

runs them.
## License:
(The MIT License)

Copyright © 2011 Sebastian Pawluś

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ‘Software’), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ‘AS IS’, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
