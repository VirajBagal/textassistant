#!/bin/bash

apt-get install ninja-build
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
pip install "unstructured[local-inference]"
apt-get update
apt-get install libleptonica-dev tesseract-ocr libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn -y
pip install tesseract
pip install tesseract-ocr

