# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contact']

package_data = \
{'': ['*'],
 'contact': ['locale/fr/LC_MESSAGES/*',
             'static/css/*',
             'templates/contact/*',
             'test_templates/*']}

install_requires = \
['django>=2.2']

setup_kwargs = {
    'name': 'myks-contact',
    'version': '1.5',
    'description': 'Simple contact form',
    'long_description': "mYk's contact form\n==================\n\nGoals\n-----\n\n`myks-contact`_ is a simple contact form. It's adequate for a personal home\npage. It features a basic CAPTCHA_.\n\n.. _myks-contact: https://github.com/aaugustin/myks-contact\n.. _CAPTCHA: http://en.wikipedia.org/wiki/Captcha\n\nSetup\n-----\n\nmyks-contact is a pluggable Django application. It is tested with Django ≥ 2.2.\n\n1.  Download and install the package from PyPI::\n\n        $ pip install myks-contact\n\n2.  Add ``contact`` to ``INSTALLED_APPS``::\n\n        INSTALLED_APPS += ['contact']\n\n    This allows Django to discover the built-in templates and translations.\n\n3. Define the list of recipients in the ``CONTACT_EMAILS`` setting::\n\n        CONTACT_EMAILS = ['you@example.com']\n\n4.  Add the application to your URLconf with the ``contact`` application\n    namespace::\n\n        urlpatterns += [\n            path('contact/', include('contact.urls', namespace='contact')),\n        ]\n\nTo use the built-in templates, your project's ``base.html`` template must\nprovide three blocks: ``title``, ``extrahead`` and ``content``, as shown in\nthis `example`_, and you must be using the staticfiles contrib app.\n\nIf these conditions are inconvenient, you can override the\n``contact/form.html`` and ``contact/thanks.html`` templates.\n\n.. _example: https://github.com/aaugustin/myks-contact/blob/master/contact/tests/templates/base.html\n\nChangelog\n---------\n\n1.5\n...\n\n* Update for Django 3.0.\n\n\n1.4\n...\n\n* Update for Django 2.0.\n\n1.3\n...\n\n* Put sender email in Reply-To instead of From.\n\n1.2\n...\n\n* Responsive CSS layout.\n\n1.1\n...\n\n* Update for Django 1.8 and later.\n\n1.0\n...\n\n* Stable release.\n\n0.3\n...\n\n* Refactored tests for Django 1.6.\n\n0.2\n...\n\n* Bundled stylesheet.\n\n0.1\n...\n\n* Initial public release, extracted from my private repository.\n* Switched the implementation to class-based generic views.\n* Added documentation (README file).\n",
    'author': 'Aymeric Augustin',
    'author_email': 'aymeric.augustin@m4x.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aaugustin/myks-contact',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
