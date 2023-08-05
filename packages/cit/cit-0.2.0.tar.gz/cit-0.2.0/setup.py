# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cit']

package_data = \
{'': ['*']}

install_requires = \
['sh>=1.14.1,<2.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['cit = cit.main:app']}

setup_kwargs = {
    'name': 'cit',
    'version': '0.2.0',
    'description': '让github的下载速度比之前快一千倍',
    'long_description': '## 序言\ngithub上有很多好项目,但是国内用户连github却非常的慢.每次都要用插件或者其他工具来解决.\n这次自己做一个小工具,输入github原地址后,就可以自动替换为代理地址,方便大家更快速的下载.\n\n<!-- more -->\n## 主要功能\n1. 将用户输入的github地址替换为代理地址',
    'author': '中箭的吴起',
    'author_email': 'solider245@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/solider245/cit.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
