# main.py — entri news-image-20261123 (Python 3.13, stdlib saja).
# Program menyalin gambar berita yang sudah dirender (entry.png, dibuat
# oleh build_image.py selama sesi build) ke /output/entry.png.
# Di luar container grader, MAKEFUN_OUTPUT_DIR menggantikan /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

os.makedirs(os.path.dirname(DST), exist_ok=True)
shutil.copyfile(SRC, DST)
print("wrote", DST)
