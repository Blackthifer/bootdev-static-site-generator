import shutil
import os
import sys
from textconversion import *

def clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def copy_static_resources(src, dst):
    clean_dir(dst)
    for path in os.listdir(src):
        src_path = os.path.join(src, path)
        dst_path = os.path.join(dst, path)
        print(f"Copying from {src_path} to {dst_path}")
        if os.path.isdir(src_path):
            copy_static_resources(src_path, dst_path)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)

def generate_page(from_path, template_path, dest_path, base_path):
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
    complete_html = complete_html.replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as dest:
        dest.write(complete_html)

def generate_pages_r(content_dir, template_path, dest_dir, base_path):
    join = os.path.join
    if os.path.isfile(content_dir):
        generate_page(content_dir, template_path, dest_dir.replace(".md", ".html"), base_path)
    elif os.path.exists(content_dir):
        sub_dirs = os.listdir(content_dir)
        for dir in sub_dirs:
            generate_pages_r(join(content_dir, dir), template_path, join(dest_dir, dir), base_path)

def main():
    cli_args = sys.argv
    basepath = "/"
    if len(cli_args) > 1:
        basepath = cli_args[1]
    print("Hi")
    copy_static_resources("static", "docs")
    generate_pages_r("content", "template.html", "docs", basepath)

main()