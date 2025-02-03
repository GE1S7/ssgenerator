from blocks import markdown_to_html_node
import os
import re

def extract_title(markdown):
    '''extract h1 header from markdown file'''

    h1_ptrn = r"^# .*"
    h1_search = re.findall(h1_ptrn, markdown)

    if h1_search != None:
        return h1_search[0].strip(" # ")

    else:
        raise Exception("no h1 header")

def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        md = file.read()

    with open(template_path, "r") as file:
        template = file.read()


    html_node = markdown_to_html_node(md)
    html = html_node.to_html()
    title = extract_title(md)
    
    #TODO Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.

    template = re.sub("{{ Title }}", title, template)
    template = re.sub("{{ Content }}", html, template)

    print(template)

    with open(dest_path, "w+") as file:
        file.write(template)
        file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entries = os.listdir(dir_path_content)
    for entry in entries:
        epath = os.path.join(dir_path_content, entry)
        edst = os.path.join(dest_dir_path, "index.html")
        if os.path.isfile(epath):
            generate_page(epath, template_path, edst)
        else:
          new_src = os.path.join(dir_path_content,entry)
          new_dst = os.path.join(dest_dir_path,entry)
          os.mkdir(new_dst)
          generate_pages_recursive(new_src, template_path, new_dst)



