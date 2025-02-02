import re
from blocks import markdown_to_html_node
import os

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

    template.replace("{{ Title }}", title)
    template.replace("{{ Content }}", html)

    with open(dest_path, "w+") as file:
        file.write(template)
        file.close()

    os.system('lynx dest_path')




    #TODO Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.

