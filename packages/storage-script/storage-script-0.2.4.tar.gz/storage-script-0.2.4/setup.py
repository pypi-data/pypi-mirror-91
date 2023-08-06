# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['storage_script', 'storage_script.cli']

package_data = \
{'': ['*']}

install_requires = \
['boto3==1.16.51']

entry_points = \
{'console_scripts': ['rasa_storage = storage_script.__main__:main']}

setup_kwargs = {
    'name': 'storage-script',
    'version': '0.2.4',
    'description': 'Rasa Storage Script',
    'long_description': '# storage-script\n\nScript for uploading/downloading models to/from AWS S3 Cloud Storage\n\n- [Installation](#installation)\n- [Usage](#usage)\n\n## Environment Variables\n\nPlease make sure to add the following variables in your environment\n\n```\nexport AWS_ACCESS_KEY_ID=\nexport AWS_SECRET_ACCESS_KEY=\nexport AWS_DEFAULT_REGION=\nexport AWS_S3_BUCKET_RASA_MODELS=\nexport AWS_ENDPOINT_URL=\n```\n\n## Requirements\n\n* Local Python Installation\n* [Boto3](https://pypi.org/project/boto3/)\n\n## Installation\n```\npip install git+https://github.tools.sap/dsx/storage-script.git\n```\n\n## Usage\n\n```\nrasa_storage [-h] [--version] {upload,download} \n\n    positional arguments:\n    {upload,download}  Rasa Storage Commands\n        upload           Uploads RASA models to AWS S3\n        download         Downloads RASA models from AWS S3\n    optional arguments:\n    -h, --help         show this help message and exit\n    --version, -v      Package Version\n````\n\n### Upload\n\n```\nrasa_storage upload [-h] --model MODEL [--folder FOLDER]\n    -h, --help            show this help message and exit\n    --model MODEL, -m MODEL\n                            Relative path to the Model (.tar.gz file) (default:\n                            None)\n    \n    optional arguments:\n    --folder FOLDER, -f FOLDER\n                            Optional: Folder Name where the model needs to be\n                            saved in AWS S3 (default: master)\n````\n\n### Download\n\n```\nrasa_storage download [-h] --model MODEL [--folder FOLDER]\n\n    -h, --help            show this help message and exit\n    --model MODEL, -m MODEL\n                            Model Name(.tar.gz file) (default: None)\n    optional arguments:\n    --folder FOLDER, -f FOLDER\n                            Optional: Folder Name from where the model needs to be\n                        downloaded (default: master)\n```',
    'author': 'Venkatesh',
    'author_email': 'venkatesh.damodar.pai@sap.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.tools.sap/dsx/storage-script',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
