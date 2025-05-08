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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    if os.path.exists(from_path):
        with open(from_path) as file:
            markdown = file.read()
    if os.path.exists(template_path):
        with open(template_path) as templ:
            template = templ.read()
    title = extract_title(markdown)
    generated_html = markdown_to_html_node(markdown).to_html()
    complete_html = template.replace("{{ Title }}", title).replace("{{ Content }}", generated_html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as dest:
        dest.write(complete_html)

def main():
    print("Hi")
    copy_static_resources("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


main()