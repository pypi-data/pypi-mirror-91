# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pangpuriye', 'pangpuriye.ai', 'pangpuriye.common', 'pangpuriye.tests']

package_data = \
{'': ['*'], 'pangpuriye': ['example/*']}

setup_kwargs = {
    'name': 'pangpuriye',
    'version': '0.1.6',
    'description': "Let's make AI easy.",
    'long_description': "# **pangpuriye**\n\nLet's make AI easy.\n\n## **Features**\n\n - **OCR** - EasyOCR + Tesseract + Levenshtein, [example](https://github.com/patharanordev/pangpuriye/blob/main/python/pangpuriye/pangpuriye/example/ocr.ipynb).\n\n## **Requirements**\n\nBefore start we require 2-main libraries below :\n - **poppler** - it used in `pdf2image`, [how-to-install](https://pypi.org/project/pdf2image/) in each OS.\n - **tesseract** - specially in MacOS, we need to install multi-language via `brew` command :\n  \n    ```bash\n    $ brew install tesseract-lang\n    ```\n\n## **Usage**\n\nWe requires library below in `pangpuriye.ai` package and our example code, you should install the library below first  :\n - pdf2image\n - python-Levenshtein\n - easyocr\n - opencv-python\n - torchvision\n - detecto\n - matplotlib\n - numpy\n\nOr\n\n```bash\n$ pip install pdf2image python-Levenshtein easyocr opencv-python torchvision detecto matplotlib numpy\n```\n\nAfter that let's install `pangpuriye` :\n\n```bash\n$ pip install pangpuriye\n```\n\nEnjoy!!!\n\n## **FAQ**\n\n**Why not pack the required liraries above into this package?**\n\nBecause of some libraries above rely on host's environment, example `pdf2image` requires `poppler` but you need to find `poppler` package that match with your host. So we did not pack the library above into our package.\n\n\n## **License**\n\nMIT",
    'author': 'Pathara Norasethasopon',
    'author_email': 'patharanor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/patharanordev/pangpuriye/blob/main/python/pangpuriye/pangpuriye',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
