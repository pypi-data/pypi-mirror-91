# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_prometheus']

package_data = \
{'': ['*']}

install_requires = \
['prometheus_client>=0.9.0,<0.10.0', 'starlette>=0.12.2']

setup_kwargs = {
    'name': 'starlette-prometheus-middleware',
    'version': '0.9.0',
    'description': 'Prometheus integration for Starlette',
    'long_description': '# Starlette Prometheus\n[![Build Status](https://github.com/Faylixe/starlette-prometheus/workflows/Continuous%20Integration/badge.svg)](https://github.com/Faylixe/starlette-prometheus-middleware/actions)\n[![Package Version](https://img.shields.io/pypi/v/starlette-prometheus-middleware?logo=PyPI&logoColor=white)](https://pypi.org/project/starlette-prometheus-middleware/)\n[![PyPI Version](https://img.shields.io/pypi/pyversions/starlette-prometheus-middleware?logo=Python&logoColor=white)](https://pypi.org/project/starlette-prometheus-middleware/)\n\n> :warning: This repository is a fork of the original\n> [starlette_prometheus middleware](https://github.com/perdy/starlette-prometheus),\n> using upgraded dependencies.\n\n## Introduction\n\nPrometheus integration for Starlette.\n\n## Requirements\n\n* Python 3.6+\n* Starlette 0.9+\n\n## Installation\n\n```console\n$ pip install starlette-prometheus-middleware\n```\n\n## Usage\n\nA complete example that exposes prometheus metrics endpoint under `/metrics/` path.\n\n```python\nfrom starlette.applications import Starlette\nfrom starlette_prometheus import metrics, PrometheusMiddleware\n\napp = Starlette()\n\napp.add_middleware(PrometheusMiddleware)\napp.add_route("/metrics/", metrics)\n```\n\nMetrics for paths that do not match any Starlette route can be filtered by passing\n`filter_unhandled_paths=True` argument to `add_middleware` method.\n\n## Contributing\n\nThis project is absolutely open to contributions so if you have a nice idea, create an issue to let the community \ndiscuss it.\n',
    'author': 'José Antonio Perdiguero López',
    'author_email': 'perdy@perdy.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/faylixe/starlette-prometheus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
