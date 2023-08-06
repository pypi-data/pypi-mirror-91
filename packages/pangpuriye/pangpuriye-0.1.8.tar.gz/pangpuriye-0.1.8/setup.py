# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pangpuriye', 'pangpuriye.ai', 'pangpuriye.common', 'pangpuriye.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pangpuriye',
    'version': '0.1.8',
    'description': "Let's make AI easy.",
    'long_description': "# **pangpuriye**\n\nLet's make AI easy.\n\n## **Features**\n\n - **OCR** - EasyOCR + Tesseract + Levenshtein, [example](https://github.com/patharanordev/pangpuriye/blob/main/python/pangpuriye/example/ocr.ipynb).\n\n## **Requirements**\n\nBefore start we require 2-main libraries below :\n - **poppler** - it used in `pdf2image`, [how-to-install](https://pypi.org/project/pdf2image/) in each OS.\n - **tesseract** - specially in MacOS, we need to install multi-language via `brew` command :\n  \n    ```bash\n    $ brew install tesseract-lang\n    ```\n\n## **Usage**\n\nWe requires library below in `pangpuriye.ai` package and our example code, you should install the library below first  :\n - pdf2image\n - python-Levenshtein\n - easyocr\n - opencv-python\n - torchvision\n - detecto\n - matplotlib\n - numpy\n\nOr\n\n```bash\n$ pip install pdf2image python-Levenshtein easyocr opencv-python torchvision detecto matplotlib numpy\n```\n\nAfter that let's install `pangpuriye` :\n\n```bash\n$ pip install pangpuriye\n```\n\nEnjoy!!!\n\n## **Issues**\n\n- **python levenshtein issue on window** :\n\n    https://stackoverflow.com/questions/13200330/how-to-install-python-levenshtein-on-windows\n\n - **poppler usage in MacOS version lower than 10.15** :\n\n    ```bash\n    Warning: You are using macOS 10.13.\n    We (and Apple) do not provide support for this old version.\n    You will encounter build failures with some formulae.\n    Please create pull requests instead of asking for help on Homebrew's GitHub,\n    Twitter or any other official channels. You are responsible for resolving\n    any issues you experience while you are running this\n    old version.\n\n    Error: poppler: no bottle available!\n    You can try to install from source with:\n\n    brew install --build-from-source poppler\n    ```\n\n## **FAQ**\n\n**Why not pack the required liraries above into this package?**\n\nBecause of some libraries above rely on host's environment, example `pdf2image` requires `poppler` but you need to find `poppler` package that match with your host. So we did not pack the library above into our package.\n\n\n## **License**\n\nMIT",
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
