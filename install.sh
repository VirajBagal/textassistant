#!/bin/bash

sudo apt-get install ninja-build
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
pip install "unstructured[local-inference]"
sudo apt-get update
sudo apt-get install libleptonica-dev tesseract-ocr libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn
pip install tesseract
pip install tesseract-ocr

