# **pangpuriye**

Let's make AI easy.

## **Features**

 - **OCR** - EasyOCR + Tesseract + Levenshtein, [example](https://github.com/patharanordev/pangpuriye/blob/main/python/pangpuriye/example/ocr.ipynb).

## **Requirements**

Before start we require 2-main libraries below :
 - **poppler** - it used in `pdf2image`, [how-to-install](https://pypi.org/project/pdf2image/) in each OS.
 - **tesseract** - specially in MacOS, we need to install multi-language via `brew` command :
  
    ```bash
    $ brew install tesseract-lang
    ```

## **Usage**

We requires library below in `pangpuriye.ai` package and our example code, you should install the library below first  :
 - pdf2image
 - python-Levenshtein
 - easyocr
 - opencv-python
 - torchvision
 - detecto
 - matplotlib
 - numpy

Or

```bash
$ pip install pdf2image python-Levenshtein easyocr opencv-python torchvision detecto matplotlib numpy
```

After that let's install `pangpuriye` :

```bash
$ pip install pangpuriye
```

Enjoy!!!

## **Issues**

- **python levenshtein issue on window** :

    https://stackoverflow.com/questions/13200330/how-to-install-python-levenshtein-on-windows

 - **poppler usage in MacOS version lower than 10.15** :

    ```bash
    Warning: You are using macOS 10.13.
    We (and Apple) do not provide support for this old version.
    You will encounter build failures with some formulae.
    Please create pull requests instead of asking for help on Homebrew's GitHub,
    Twitter or any other official channels. You are responsible for resolving
    any issues you experience while you are running this
    old version.

    Error: poppler: no bottle available!
    You can try to install from source with:

    brew install --build-from-source poppler
    ```

## **FAQ**

**Why not pack the required liraries above into this package?**

Because of some libraries above rely on host's environment, example `pdf2image` requires `poppler` but you need to find `poppler` package that match with your host. So we did not pack the library above into our package.


## **License**

MIT