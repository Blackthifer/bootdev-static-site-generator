import shutil
import os
from textconversion import *

def clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def copy_static_resources(src, dst):
    clean_dir(dst)
    for path in os.listdir(src):
        src_path = os.path.join(src, path)
        print(src_path)
        dst_path = os.path.join(dst, path)
        if os.path.isdir(src_path):
            copy_static_resources(src_path, dst_path)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)

def main():
    print("Hi")
    copy_static_resources("static", "public")
    print(extract_title("# Hello"))

main()