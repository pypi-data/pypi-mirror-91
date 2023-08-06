# django-patternfly

![CI](https://github.com/Rintsi/django-patternfly/workflows/CI/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/Rintsi/django-patternfly/badge.svg?branch=master)](https://coveralls.io/github/Rintsi/django-patternfly?branch=master)

Patternfly integration for Django. Ported from [django-bootstrap4](https://github.com/zostera/django-bootstrap4)

DISCLAIMER: This is a port done over the weekend and is a very poorly featured
package. The only purpose for this currently is to provide a CSS to be used in
your project templates

## Goal

The goal of this project is to seamlessly blend Django and PatternFly.

## Requirements

Python 3.6 or newer with Django >= 2.2 or newer.

## Documentation

The full documentation is (will be) at https://django-patternly.readthedocs.io/

## Installation

1. Install using pip:

   ```shell script
   pip install django-patternfly
   ```


2. Add to `INSTALLED_APPS` in your `settings.py`:

   ```python
   INSTALLED_APPS = (
       # ...
       "patternfly",
       # ...
   )
   ```

3. In your templates, load the `patternfly` library and use the `patternfly_*` tags:

## Example template

```djangotemplate
{% load patternfly %}

<html>
    <head>
        {% patternfly_css %}
    </head>
    <body>
        {% block patternfly_content %}
            Main Content
        {% endblock %}
    </body>
</html>
```

## Development

Install poetry

```shell script
$ conda install -c conda-forge poetry
```

## Bugs and suggestions

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/Rintsi/django-patternfly/issues

## License

You can use this under BSD-3-Clause. See [LICENSE](LICENSE) file for details.

## Author

Developed and maintained by [Rintsi](https://linkedin.com/in/rintsi).

Please see [AUTHORS.md](AUTHORS.md) for a list of contributors.
