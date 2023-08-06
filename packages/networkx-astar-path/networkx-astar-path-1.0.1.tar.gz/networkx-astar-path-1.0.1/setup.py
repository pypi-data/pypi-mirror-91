# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['networkx_astar_path']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5']

setup_kwargs = {
    'name': 'networkx-astar-path',
    'version': '1.0.1',
    'description': 'Alternative A* implementation, which provides the current and previous edge to the weight function.',
    'long_description': '# networkx-astar-path\n\n![PyPI](https://img.shields.io/pypi/v/networkx-astar-path?style=flat-square)\n![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/escaped/networkx-astar-path/Test%20&%20Lint/master?style=flat-square)\n![Coveralls github branch](https://img.shields.io/coveralls/github/escaped/networkx-astar-path/master?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/networkx-astar-path?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/networkx-astar-path?style=flat-square)\n\nAlternative A* implementation, which provides the current and previous edge to the weight function.\n\n## Requirements\n\n* Python 3.6.1 or newer\n\n## Installation\n\n```sh\npip install networkx-astar-path\n```\n\n## Usage\n\nnetworkx\'s implementation of A* limit the arguments of the weight function to the current edge onlye.\nSome scenarious require that the cost for the current edge is dependent on the prevous edge.\nAn example is the bearing between two edges.\nSurely, the bearing could be pre-calculate and stored on the node, but this is sometimes not possible.\n\nThe API of this implementation is the same, with the one exception that the weight-funciton signature has changed to\n\n```python\ndef weight(graph: nx.Graph, prev_edge: Optional[Tuple[Any, Any]], cur_edge: Tuple[Any, Any]) -> float:\n    ...\n```\n\nIf the weight-function is called for the first time, the value for `prev_edge` is `None` as we haven\'t visited any other edge yet.\n\n### Example\n\n> **NOTE** This example is not very practical, but shows how this function can be used.\n\nGiven the following graph\n\n![Graph](docs/graph.png)\n\n```python\nimport networks as nx\n\ngraph = nx.DiGraph()\n\ngraph.add_edges_from([(\'S\', \'A1\')], weight=-2)\ngraph.add_edges_from([(\'A1\', \'T\')], weight=7)\ngraph.add_edges_from([(\'S\',\'A2\'), (\'A2\',\'B2\'),(\'B2\',\'C2\'),(\'C2\',\'T\')], weight=1)\n```\n\n\nwe are searching for the shortest path from `S` to `T`.\n\n> The [weights have been chosen](https://www.wolframalpha.com/input/?i=x%2By%2Bz+%3C+a+%2B+b%3B+x+%2B+y%2Fx+%2B+z%2Fy+%3E+a+%2B+b%2Fa%3B++x%3D1%2C+y%3D1%2C+z%3D) in a way that the path `[\'S\', \'A2\', \'B2\', \'C2\', \'T\']` is shorter when we simply sum up the weights, but longer if the weight of the current edge is divided by the weight of the previous edge.\nThe shortest path for the latter is `[\'S\', \'A1\', \'T\']`.\n\nLet\'s find the shortest path by only looking at the weights of the current edge.\n\n```python\nfrom networkx_astar_path import astar_path\n\npath = astar_path(graph, source=\'S\', target=\'T\', weight="weight")\n# [\'S\', \'A2\', \'B2\', \'C2\', \'T\']\n```\n\n![Shortest path based on the current edge](docs/graph_simple_weights.png)\n\nWe now define a "simple" weight function, which takes the previous edge into account:\n\n> If we already visited an edge, the weight is the weight of the current edge divided by the weight of the previous edge.\n> Otherwise, the weight of the current edge is returned.\n\n```python\nfrom networkx_astar_path import astar_path\n\ndef dependent_weight(graph: nx.Graph, prev_edge: Optional[Tuple[Any, Any]], cur_edge: Tuple[Any, Any]) -> float:\n    if prev_edge is None:\n        return graph.get_edge_data(*cur_edge)[\'weight\']\n\n    prev_weight = graph.get_edge_data(*prev_edge)[\'weight\']\n    cur_weight = graph.get_edge_data(*cur_edge)[\'weight\']\n    return cur_weight / prev_weight\n\npath = astar_path(graph, source=\'S\', target=\'T\', weight=dependent_weight)\n# [\'S\', \'A1\', \'T\']\n```\n\n![Shortest path based on the previous edge](docs/graph_dependant_weights.png)\n\n## Development\n\nThis project uses [poetry](https://poetry.eustace.io/) for packaging and\nmanaging all dependencies and [pre-commit](https://pre-commit.com/) to run\n[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),\n[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).\n\nClone this repository and run\n\n```bash\npoetry install\npoetry run pre-commit install\n```\n\nto create a virtual enviroment containing all dependencies.\nAfterwards, You can run the test suite using\n\n```bash\npoetry run pytest\n```\n\nThis repository follows the [Conventional Commits](https://www.conventionalcommits.org/)\nstyle.\n\n### Cookiecutter template\n\nThis project was created using [cruft](https://github.com/cruft/cruft) and the\n[cookiecutter-pyproject](https://github.com/escaped/cookiecutter-pypackage) template.\nIn order to update this repository to the latest template version run\n\n```sh\ncruft update\n```\n\nin the root of this repository.\n',
    'author': 'Alexander Frenzel',
    'author_email': 'alex@relatedworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/escaped/networkx-astar-path',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
