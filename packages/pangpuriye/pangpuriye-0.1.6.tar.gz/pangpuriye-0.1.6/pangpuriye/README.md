# **pangpuriye**

Let's make AI easy.

## **Features**

 - **OCR** - EasyOCR + Tesseract + Levenshtein, [example](https://github.com/patharanordev/pangpuriye/blob/main/python/pangpuriye/pangpuriye/example/ocr.ipynb).

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

## **FAQ**

**Why not pack the required liraries above into this package?**

Because of some libraries above rely on host's environment, example `pdf2image` requires `poppler` but you need to find `poppler` package that match with your host. So we did not pack the library above into our package.


## **License**

MIT