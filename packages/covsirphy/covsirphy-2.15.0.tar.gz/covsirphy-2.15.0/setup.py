# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covsirphy',
 'covsirphy.analysis',
 'covsirphy.cleaning',
 'covsirphy.ode',
 'covsirphy.phase',
 'covsirphy.simulation',
 'covsirphy.util',
 'covsirphy.worldwide']

package_data = \
{'': ['*']}

install_requires = \
['better-exceptions>=0.3.2,<0.4.0',
 'country-converter>=0.7.1,<0.8.0',
 'covid19dh>=2.0.3,<3.0.0',
 'dask[dataframe]>=2020.12.0,<2021.0.0',
 'fsspec[http]>=0.8.5,<0.9.0',
 'japanmap>=0.0.21,<0.0.22',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'optuna>=2.3.0,<3.0.0',
 'pandas>=1.1.5,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'ruptures>=1.1.1,<2.0.0',
 'scikit-learn>=0.24.0,<0.25.0',
 'scipy>=1.5.4,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'tabulate>=0.8.7,<0.9.0',
 'wbdata>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'covsirphy',
    'version': '2.15.0',
    'description': 'COVID-19 data analysis with phase-dependent SIR-derived ODE models',
    'long_description': '\n<img src="./docs/logo/covsirphy_headline.png" width="390" alt="CovsirPhy: COVID-19 analysis with phase-dependent SIRs">\n\n[![PyPI version](https://badge.fury.io/py/covsirphy.svg)](https://badge.fury.io/py/covsirphy)\n[![Downloads](https://pepy.tech/badge/covsirphy)](https://pepy.tech/project/covsirphy)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/covsirphy)](https://badge.fury.io/py/covsirphy)\n[![Build Status](https://semaphoreci.com/api/v1/lisphilar/covid19-sir/branches/master/shields_badge.svg)](https://semaphoreci.com/lisphilar/covid19-sir)  \n[![GitHub license](https://img.shields.io/github/license/lisphilar/covid19-sir)](https://github.com/lisphilar/covid19-sir/blob/master/LICENSE)\n[![Maintainability](https://api.codeclimate.com/v1/badges/eb97eaf9804f436062b9/maintainability)](https://codeclimate.com/github/lisphilar/covid19-sir/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/eb97eaf9804f436062b9/test_coverage)](https://codeclimate.com/github/lisphilar/covid19-sir/test_coverage)\n[![Open Source Helpers](https://www.codetriage.com/lisphilar/covid19-sir/badges/users.svg)](https://www.codetriage.com/lisphilar/covid19-sir)\n\n# CovsirPhy introduction\n\n[<strong>Documentation</strong>](https://lisphilar.github.io/covid19-sir/index.html)\n| [<strong>Installation</strong>](https://lisphilar.github.io/covid19-sir/INSTALLATION.html)\n| [<strong>Quickest usage</strong>](https://lisphilar.github.io/covid19-sir/usage_quickest.html)\n| [<strong>API reference</strong>](https://lisphilar.github.io/covid19-sir/covsirphy.html)\n| [<strong>GitHub</strong>](https://github.com/lisphilar/covid19-sir)\n| [<strong>Qiita (Japanese)</strong>](https://qiita.com/tags/covsirphy)\n\n<strong>CovsirPhy is a Python library for COVID-19 (Coronavirus disease 2019) data analysis with phase-dependent SIR-derived ODE models. We can download datasets and analyse them easily. Scenario analysis with CovsirPhy enables us to make data-informed decisions. Please refer to "Method" part of [Kaggle Notebook: COVID-19 data with SIR model](https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model) to understand the methods.</strong>\n\n<img src="./docs/gif/covsirphy_demo.gif" width="600">\n\n## Functionalities\n- [Data preparation and data visualization](https://lisphilar.github.io/covid19-sir/usage_dataset.html)\n- [Phase setting with S-R Trend analysis](https://lisphilar.github.io/covid19-sir/usage_phases.html)\n- [Numerical simulation of ODE models](https://lisphilar.github.io/covid19-sir/usage_theoretical.html)\n    - Stable: SIR, SIR-D and SIR-F model\n    - Development: SIR-FV and SEWIR-F model\n- [Phase-dependent parameter estimation of ODE models](https://lisphilar.github.io/covid19-sir/usage_quickest.html)\n- [Scenario analysis](https://lisphilar.github.io/covid19-sir/usage_quick.html): Simulate the number of cases with user-defined parameter values\n- [(In development): Find the relationship of government response and parameter values](https://lisphilar.github.io/covid19-sir/usage_policy.html)\n\n## Inspiration\n- Monitor the spread of COVID-19\n- Keep track parameter values/reproduction number in each country/province\n- Find the relationship of reproductive number and measures taken by each country\n\n<strong>If you have ideas or need new functionalities, please join this project.\nAny suggestions with [Github Issues](https://github.com/lisphilar/covid19-sir/issues/new/choose) are always welcomed. Please read [Guideline of contribution](https://lisphilar.github.io/covid19-sir/CONTRIBUTING.html) in advance.</strong>\n\n## Installation\nThe latest stable version of CovsirPhy is available at [PyPI (The Python Package Index): covsirphy](https://pypi.org/project/covsirphy/) and supports Python 3.7 or newer versions. Details are explained in [Documentation: Installation](https://lisphilar.github.io/covid19-sir/INSTALLATION.html).\n\n```\npip install --upgrade covsirphy\n```\n\n## Usage\nQuickest tour of CovsirPhy is here. The following codes analyze the records in Japan, but we can change the country name when creating `Scenario` class instance for your own analysis.\n\n```Python\nimport covsirphy as cs\n# Download and update datasets\ndata_loader = cs.DataLoader("input")\njhu_data = data_loader.jhu()\npopulation_data = data_loader.population()\n# Check records\nsnl = cs.Scenario(jhu_data, population_data, country="Japan")\nsnl.records()\n# S-R trend analysis\nsnl.trend().summary()\n# Parameter estimation of SIR-F model\nsnl.estimate(cs.SIRF)\n# History of reproduction number\n_ = snl.history(target="Rt")\n# History of parameters\n_ = snl.history_rate()\n_ = snl.history(target="rho")\n# Simulation for 30 days\nsnl.add(days=30)\n_ = snl.simulate()\n```\n\nFurther information:\n\n- [CovsirPhy documentation](https://lisphilar.github.io/covid19-sir/index.html)\n- Example scripts in ["example" directory of this repository](https://github.com/lisphilar/covid19-sir/tree/master/example)\n- [Kaggle: COVID-19 data with SIR model](https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model)\n\n\n## Support\nPlease support this project as a developer (or a backer).\n[![Become a backer](https://opencollective.com/covsirphy/tiers/backer.svg?avatarHeight=36&width=600)](https://opencollective.com/covsirphy)\n\n\n## License: Apache License 2.0\nPlease refer to [LICENSE](https://github.com/lisphilar/covid19-sir/blob/master/LICENSE) file.\n\n## Citation\nWe have no original papers the author and contributors wrote, but please cite this package as follows.\n\nCovsirPhy Development Team (2020), CovsirPhy, Python package for COVID-19 analysis with SIR-derived ODE models, https://github.com/lisphilar/covid19-sir\n\nIf you want to use SIR-F/SIR-FV/SEWIR-F model, S-R trend analysis, phase-dependent approach to SIR-derived models, and other scientific method performed with CovsirPhy, please cite the next Kaggle notebook.\n\nLisphilar (2020), Kaggle notebook, COVID-19 data with SIR model, https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model\n\n## Related work\n\nReproduction number evolution in each country:  \nIlyass Tabiai and Houda Kaddioui (2020), GitHub pages, COVID19 R0 tracker, https://ilylabs.github.io/projects/COVID-trackers/\n',
    'author': 'Lisphilar',
    'author_email': 'lisphilar@outlook.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lisphilar/covid19-sir',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
