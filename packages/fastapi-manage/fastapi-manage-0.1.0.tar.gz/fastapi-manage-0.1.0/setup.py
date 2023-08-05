# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_manage']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'configobj>=5.0.6,<6.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['fastapi-manage = fastapi_manage.main:app']}

setup_kwargs = {
    'name': 'fastapi-manage',
    'version': '0.1.0',
    'description': '',
    'long_description': '# fastapi_manage\n\n#### 介绍\nfastapi的模板生成，数据库版本管理项目\nfastapi+sqlalchemy\n',
    'author': 'lewei_huang',
    'author_email': 'auxpd96@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
