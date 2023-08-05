# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turtle_language_server']

package_data = \
{'': ['*']}

install_requires = \
['pygls>=0.9.1,<0.10.0', 'rdflib>=5.0.0,<6.0.0']

entry_points = \
{'console_scripts': ['turtle_langserver = turtle_language_server.entry:main']}

setup_kwargs = {
    'name': 'turtle-language-server',
    'version': '0.1.1',
    'description': 'Language Server Protocol implementation for Turtle and RDF',
    'long_description': '# Turtle Language Server\n\nThis is a [LSP server](https://langserver.org/) implementation for RDF graphs serialized as Turtle.\n\nInstall with: `pip install turtle_language_server`\n\n\n## With NeoVim and CoC\n\nIf you are using [`coc.nvim`](https://github.com/neoclide/coc.nvim), you can configure the language server as follows:\n\n1. Make sure Vim correctly detects turtle files and sets the filetype. One way to achieve this \n   is by adding the following line to your `.vimrc` or `init.nvim`:\n   \n   ```vimrc\n   au BufRead,BufNewFile *.ttl set filetype=turtle\n   ```\n2. Modify your CoC settings to use the `turtle_language_server` when you open a Turtle file.\n    1. First, run `:CocConfig` or edit `coc-settings.json`\n    2. Add the following (merge with existing keys in `"languageserver"` if needed):\n        ```json\n        {\n          "languageserver": {\n            "turtle": {\n              "command": "turtle_langserver",\n              "filetypes": ["ttl", "turtle"]\n            }\n          }\n        }\n        ```\n',
    'author': 'Gabe Fierro',
    'author_email': 'gtfierro@cs.berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://brickschema.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
