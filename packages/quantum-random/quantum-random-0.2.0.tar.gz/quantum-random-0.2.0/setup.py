# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['qrandom']
install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'quantum-random',
    'version': '0.2.0',
    'description': 'Quantum random numbers',
    'long_description': "# Quantum random numbers in Python\n\n![Tests](https://github.com/sbalian/quantum-random/workflows/Tests/badge.svg)\n\nThis package brings the [ANU quantum random numbers][anu] to Python 3.6+.\n\nThe default pseudo-random generator in Python is replaced by calls to the\nANU API that serves real quantum random numbers.\n\n```bash\npip install quantum-random\n```\n\nJust import `qrandom` and use it like you'd use the\n[standard Python random module][pyrandom]. For example,\n\n```python\n>>> import qrandom\n\n>>> qrandom.random()\n0.15357449726583722\n\n>>> qrandom.sample(range(10), 2)\n[6, 4]\n\n>>> qrandom.gauss(0.0, 1.0)\n-0.8370871276247828\n```\n\nThe `qrandom` module exposes a class (`qrandom.QuantumRandom`) derived from\n`random.Random` with a `random` method that outputs quantum floats in the\nrange [0.0, 1) (converted from 64-bit ints). Overriding `random.Random.random`\nis sufficient to make the `qrandom` module behave like the `random` module as\ndescribed in the [Python docs][pyrandom]. A batch of 1024 quantum numbers are \nfetched from the API at a time. If you wish to pre-fetch, use `qrandom.fill(n)`, \nwhere `n` is the number of 1024-batches.\n\nTo run the tests locally, you will need [poetry][poetry] and Python 3.6-3.9.\n\n```bash\npoetry install\npoetry run tox\n```\n\nSee [here](./docs/uniform.md) for a visualisation and a Kolmogorov–Smirnov test.\n\n[anu]: https://qrng.anu.edu.au\n[pyrandom]: https://docs.python.org/3.9/library/random.html\n[poetry]: https://python-poetry.org\n",
    'author': 'Seto Balian',
    'author_email': 'seto.balian@gmail.com',
    'maintainer': 'Seto Balian',
    'maintainer_email': 'seto.balian@gmail.com',
    'url': 'https://github.com/sbalian/quantum-random',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
