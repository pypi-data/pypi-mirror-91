# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['qrandom']
install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'quantum-random',
    'version': '0.1.0',
    'description': 'Quantum random numbers',
    'long_description': "# Quantum random numbers in Python\n\nThis package brings the [ANU quantum random numbers][anu] to Python.\n\nThe default pseudo-random generator in Python is replaced by calls to the\nANU API that serves real quantum random numbers.\n\n```bash\npip install quantum-random\n```\n\nJust import `qrandom` and use it like you'd use the\n[standard Python random module][pyrandom]. For example,\n\n```python\n>>> import qrandom\n\n>>> qrandom.random()\n0.15357449726583722\n\n>>> qrandom.sample(range(10), 2)\n[6, 4]\n\n>>> qrandom.gauss(0.0, 1.0)\n-0.8370871276247828\n```\n\nSupports Python 3.6+.\n\nTo run the tests locally, you will need [poetry][poetry] and Python 3.6-3.9.\n\n```\npoetry install\npoetry shell\ntox\n```\n\n[This notebook][viz] shows the distribution in [0.0, 1.0) obtained\nby calling `qrandom.random()` 10,000 times and checks for uniformity\nusing a Kolmogorov-Smirnov test.\n\n[anu]: https://qrng.anu.edu.au\n[pyrandom]: https://docs.python.org/3.9/library/random.html\n[viz]: ./tests/notebooks/UniformTest.ipynb\n[poetry]: https://python-poetry.org\n",
    'author': 'Seto Balian',
    'author_email': 'seto.balian@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sbalian/quantum-random',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
