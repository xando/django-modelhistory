# django-modelhistory
[https://github.com/xando/django-modelhistory](http://github.com/xando/django-modelhistory)


## Description:
Simple model logging helper for django projects. Covers functionality of discovering action taken on object: DELETE, UPDATE, CREATE and creates and saves suitable message to database. Supports simple db.models.Models objects as well as forms, formset and inlineformset based on Django ORM Models

## Status:
This application is pretty much in alpha stage, so be careful :)

## Installation:

```bash
pip install django-modelhistory
```
or

```bash
easy_install django-modelhistory
```

## Configuration:

First you have to add modelhistory do your INSTALLED_APPS inside **settings.py**:

```python
INSTALLED_APPS = (
    ...
    'modelhistory'
)
```

and to create tables for history records run:

```bash
python manage.py syncdb
```

Everywhere where you want to use History you have to place this import.

```python
from django_history.models import History
```

## Usage:

### objects

```python
obj = SimpleModel.objects.create(name="So cool name")
History.log.obj(obj)
```

### forms (model forms)
```python
form = SimpleModelForm(request.POST)
...
form.save()
log = History.log.form(form)
```

### formsets (model formsets)
```python
formset = ModelFormSet(request.POST)
...
formset.save()
log = History.log.formset(formset)
```

### inline formsets (inline model formsets)
```python
obj = SimpleModel.objects.create(name="So cool name")
formset = ModelInlineFormSet(request.POST, instance=obj)
...
formset.save()
log = History.log.inlineformset(formset)
```

### implicite usage

Just create an object, form or formset. Do what to you whant to do with it and pass 

``````python
History.log(obj)
# where object could be an instance of model, form or formset.
```

## Tests:
Tests are [here](https://github.com/xando/django-modelhistory/tree/master/modelhistory/tests).

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
