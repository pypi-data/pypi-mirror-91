# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vendetta']

package_data = \
{'': ['*']}

install_requires = \
['faker>=5.5.1,<6.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'strictyaml>=1.3.1,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['vendetta = vendetta.cli:main']}

setup_kwargs = {
    'name': 'vendetta',
    'version': '0.0.1',
    'description': 'Anonymize CSV datasets',
    'long_description': "# vendetta\n\n[![Build Status](https://github.com/anatoly-scherbakov/vendetta/workflows/test/badge.svg?branch=master&event=push)](https://github.com/anatoly-scherbakov/vendetta/actions?query=workflow%3Atest)\n[![Python Version](https://img.shields.io/pypi/pyversions/vendetta.svg)](https://pypi.org/project/vendetta/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nAnonymize CSV file(s) by replacing sensitive values with fakes.\n\n## Installation\n\n```bash\npip install vendetta\n```\n\n\n## Example\n\n\nSuppose you have `orders.csv` dataset with real customer names and order IDs.\n\n```csv\nCustomerName,CustomerLastName,OrderID\nDarth,Wader,1254\nDarth,Wader,1255\n,Yoda,1256\nLuke,Skywalker,1257\nLeia,Skywalker,1258\n,Yoda,1259\n```\n\nThis list contains 4 unique customers. Let's create a configuration file, say, `orders.yaml`:\n\n```yaml\ncolumns:\n  CustomerName: first_name\n  CustomerLastName: last_name\n```\n\nand run:\n\n```shell\nvendetta orders.yaml orders.csv anon.csv\n```\n\nwhich gives something like this in `anon.csv`:\n\n```csv\nCustomerName,CustomerLastName,OrderID\nElizabeth,Oliver,1254\nElizabeth,Oliver,1255\nKaren,Rodriguez,1256\nJonathan,Joseph,1257\nKatelyn,Joseph,1258\nKaren,Rodriguez,1259\n```\n\n- OrderID column was not mentioned in the config, and was left as is\n- Using [faker](https://faker.readthedocs.io/), program replaced the first and last names with random first and last names, making the data believable\n- If in the source file two cells for the same column had the same value (Vader), the output file will also have identical values in these cells.\n\nEnjoy!\n\n## License\n\n[MIT](https://github.com/anatoly-scherbakov/vendetta/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [b80221aaae4ac702bea7e66b77b9389d527c1e3c](https://github.com/wemake-services/wemake-python-package/tree/b80221aaae4ac702bea7e66b77b9389d527c1e3c). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/b80221aaae4ac702bea7e66b77b9389d527c1e3c...master) since then.\n",
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anatoly-scherbakov/vendetta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
