# Django Profanity Filter

[![PyPI license](https://img.shields.io/pypi/l/django-profanity-filter.svg)](https://pypi.python.org/pypi/django-profanity-filter/) ![PyPI](https://img.shields.io/pypi/v/django-profanity-filter.svg) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-profanity-filter.svg) ![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-profanity-filter.svg) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Django Profanity Filter is a simple Django app that introduces a range of template tags and filters and model validators that remove or censor inappropriate language. 

## Installation
1. Install via pip
```
$ pip install django-profanity-filter
```
2. Add `'profanity',` to your `INSTALLED_APPS` in `settings.py`
```python
INSTALLED_APPS = (
...
'profanity',
...
)
```

## Usage
#### Template Tags
At the top of every template you wish to use profanity filters and tags on, make sure to load the profanity tags.

```jinja2
...
{% load profanity %}
...
```
##### Censor Filter
###### Example
```jinja2
{% with string='You are a bitch!' %}
{{ string|censor }}
{% endwith %}
```
The output will be `You are a *****!`, instead of `You are a bitch!`.

##### Is Profane Tag
###### Example
```jinja2
{% with string='You are a bitch!' %}
{{ string|is_profane }}
{% endwith %}
```
The output will be `True`, since the string contains profanity.

#### Validators
##### Is Profane Validator
###### Example
```python
from profanity.validators import validate_is_profane

class Post(models.Model):
    post = models.TextArea(max_length=150, validators=[validate_is_profane])
```
You can also now validate text within unbroken strings, i.e. strings with no spaces in them (stringswithnospacesinthem). To do so, use the validate_is_profane_nospace validator as shown below:

```python
from profanity.validators import validate_is_profane_nospace

class Post(models.Model):
    post = models.TextArea(max_length=150, validators=[validate_is_profane_nospace])
```
Because there are sometimes profane words nested within safe words (e.g. semen in basement), this validator also uses a "good list" of words that will trigger false positives. If you notice that a word is being blocked from use due to it triggering a false positive, simply add the word to goodlist.txt

## TODO
### Template Tags

- [x] Basic filter
- [ ] Advanced filter
    - Keyword argument for custom word filter
    
### Validators
- [x] Basic Censorship Validator
- [x] Nospace Profanity Validator (for usernames and other unbroken strings)
- [ ] Advanced validator - perhaps with the ability to find common morphs of words 
    
