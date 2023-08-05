# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_require_migration_name',
 'django_require_migration_name.management',
 'django_require_migration_name.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-require-migration-name',
    'version': '0.2.0',
    'description': "require `name` in Django's `makemigrations`",
    'long_description': "# django-require-migration-name\n\n[![codecov](https://codecov.io/gh/whtsky/django-require-migration-name/branch/master/graph/badge.svg?token=WXUN262JEF)](https://codecov.io/gh/whtsky/django-require-migration-name)\n\nrequire `name` in Django's `makemigrations`\n\n## Installation\n\n```bash\npip install django-require-migration-name\n```\n\n## Usage\n\nAdd `django_require_migration_name` into your `INSTALLED_APPS`:\n\n```python\nINSTALLED_APPS = [\n    # ...\n\n    'django_require_migration_name',\n]\n```\n\nThen you can't `makemigrations` without `name`:\n\n```bash\n>> python manage.py makemigrations\nCommandError: Please provide name for migration file(s).\n>> python manage.py makemigrations -n name_here\nNo changes detected\n```\n\n## Changelog\n\n### v0.2.0\n\n- fix: use underscore in package folder name\n\n### v0.1.0\n\n- Initial release\n",
    'author': 'Wu Haotian',
    'author_email': 'whtsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whtsky/django-require-migration-name',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
