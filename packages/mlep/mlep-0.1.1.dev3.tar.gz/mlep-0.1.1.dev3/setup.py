# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlep']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mlep',
    'version': '0.1.1.dev3',
    'description': 'Interact with an EnergyPlus simulation during runtime using the BCVTB protocol.',
    'long_description': '# MLEP Client\nInteract with an EnergyPlus simulation during runtime using the BCVTB protocol.\n\n# Usage\n`pip install mlep`\n\nUp to date usage can be found in the alfalfa repository, likely in [osm_model_advancer](https://github.com/NREL/alfalfa/blob/develop/alfalfa_worker/step_sim/osm_model_advancer.py) function.  As tests get added, usage will be updated.\n\n# Releasing\nSee [release info here](https://gist.github.com/corymosiman12/26fb682df2d36b5c9155f344eccbe404#releasing)\n',
    'author': 'Willy Bernal Heredia',
    'author_email': 'willy.bernalheredia@nrel.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
