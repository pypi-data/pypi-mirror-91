# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pangpuriye', 'pangpuriye.ai', 'pangpuriye.common', 'pangpuriye.tests']

package_data = \
{'': ['*'], 'pangpuriye': ['example/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'detecto>=1.2.0,<2.0.0',
 'easyocr==1.2.1',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy==1.19.0',
 'opencv-python>=4.5.1,<5.0.0',
 'pdf2image==1.14.0',
 'pytesseract>=0.3.7,<0.4.0',
 'pythainlp>=2.2.6,<3.0.0',
 'python-Levenshtein==0.12.0',
 'strsimpy>=0.2.0,<0.3.0',
 'torch==1.4',
 'torchvision==0.5.0',
 'tqdm==4.54.1']

setup_kwargs = {
    'name': 'pangpuriye',
    'version': '0.1.4',
    'description': "Let's make AI easy.",
    'long_description': "# **pangpuriye**\n\nLet's make AI easy.\n\n## **Features**\n\n - **OCR** - EasyOCR + Tesseract + Levenshtein, [example](https://github.com/patharanordev/pangpuriye/blob/main/python/pangpuriye/pangpuriye/example/ocr.ipynb).\n\n## **Requirements**\n\nBefore start we require 2-main libraries below :\n - **poppler** - it used in `pdf2image`, [how-to-install](https://pypi.org/project/pdf2image/) in each OS.\n - **tesseract** - specially in MacOS, we need to install multi-language via `brew` command :\n  \n    ```bash\n    $ brew install tesseract-lang\n    ```\n\n## **Usage**\n\nAfter that let's install `pangpuriye` :\n\n```bash\n$ pip install pangpuriye\n```\n\nEnjoy!!!\n\n## **License**\n\nMIT",
    'author': 'Pathara Norasethasopon',
    'author_email': 'patharanor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/patharanordev/pangpuriye/blob/main/python/pangpuriye/pangpuriye',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
