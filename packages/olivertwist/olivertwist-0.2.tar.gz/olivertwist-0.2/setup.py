# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olivertwist',
 'olivertwist.config',
 'olivertwist.metricengine',
 'olivertwist.reporter',
 'olivertwist.ruleengine',
 'olivertwist.rules']

package_data = \
{'': ['*'],
 'olivertwist.reporter': ['html/css/*',
                          'html/images/*',
                          'html/webfonts/*',
                          'templates/*']}

install_requires = \
['Jinja2==2.11.2',
 'PyInquirer>=1.0.3,<2.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama<0.4.4',
 'dataclasses-jsonschema>=2.13.0,<3.0.0',
 'flake8-bugbear>=20.11.1,<21.0.0',
 'networkx>=2.5,<3.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['olivertwist = olivertwist.main:main',
                     'ot = olivertwist.main:main']}

setup_kwargs = {
    'name': 'olivertwist',
    'version': '0.2',
    'description': 'DBT DAG Auditor',
    'long_description': "\n\n![Alt text](https://github.com/autotraderuk/oliver-twist/blob/main/docs/images/oliver_twist_logo.png)\n# oliver-twist\n\nDAG Auditor\n\n[![Build status badge](https://github.com/autotraderuk/oliver-twist/workflows/CI/badge.svg)](https://github.com/autotraderuk/oliver-twist/actions?query=workflow%3ACI)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI](https://img.shields.io/pypi/v/olivertwist)](https://pypi.org/project/olivertwist/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/olivertwist)](https://pypi.org/project/olivertwist/)\n[![GitHub - License](https://img.shields.io/github/license/autotraderuk/oliver-twist)](https://github.com/autotraderuk/oliver-twist/blob/main/LICENSE)\n\noliver-twist is a dag auditing tool that audits the [DBT](https://www.getdbt.com/) DAG and generates a summary report. There is a [docs site][1], including descriptions of all [currently implemented rules][2].\n\n![please sir, can I automate my DAG auditing](https://github.com/autotraderuk/oliver-twist/blob/main/docs/images/oliver_dag_meme.jpg)\n\n# Getting Started\n\nTo get started, install the package\n\n```shell\n$ pip install olivertwist\n```\n\nand then run it by passing it your dbt manifest JSON\n\n```shell\nolivertwist check manifest.json\n```\n\nThis will report any failures to the console, and also in HTML format in a directory called `target`. You can optionally auto-open the report in a browser with:\n\n```shell\nolivertwist check manifest.json --browser\n```\n\nFull options are available with:\n\n\n```shell\nolivertwist check --help\n```\n\n## Configuration\n\n[All rules][2] are enabled by default. To change this you need a configuration file called `olivertwist.yml` in the same directory you are running `olivertwist`. An example configuration is shown below:\n\n```yaml\nversion: '1.0'\nuniversal:\n  - id: no-rejoin-models\n    enabled: false\n  - id: no-disabled-models\n    enabled: true\n```\n\nThere is a command to help you generate the config automatically:\n\n```shell\nolivertwist config\n```\n\nThis will show all the available rules and allow you to toggle the ones that you want to enforce.\n\n## Local Development\n\n### Clone this repo and install the project:\n\n`poetry install`\n\n### Install pre-commit hooks for linting\n\nThis is optional, but highly recommended to avoid annoying linting failure in CI.\n\n`poetry run pre-commit install`\n\nTo run the pre-commit hooks locally:\n\n`poetry run pre-commit run`\n\n### To get the latest versions of the dependencies and to update the poetry.lock file run:\n\n`poetry update`\n\n### To run oliver-twist and generate the summary report run:\n\n`poetry run olivertwist example_manifest.json`\n\n### Working with diagrams\n \nTo update and regenerate the images that illustrate rule failures in the documentation follow the next steps:\n- update the diagrams using the [mermaid syntax](https://mermaid-js.github.io/mermaid/#/)\n- install [yarn](https://classic.yarnpkg.com/en/docs/install/)\n- `cd docs/diagrams`\n- `./generate.sh`\n- inspect the generated images in `./docs/diagrams/output/`\n- if you're happy with the results, run `./copy.sh` so that they are copied over to `./docs/images`\n- you can now reference those images. e.g. in `.docs/rules.md`\n\n### Creating a distribution\n\n```poetry build --format wheel```\n\n\n[1]: http://olivertwi.st/\n[2]: http://olivertwi.st/rules/\n",
    'author': 'Angelos Georgiadis',
    'author_email': 'angelos.georgiadis@autotrader.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://olivertwi.st',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
