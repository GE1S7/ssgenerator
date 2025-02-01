import re
from blocks import markdown_to_html_node

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

    md_f = open(from_path, "r")
    template_f = open(template_path, "r") 

    html_node = markdown_to_html_node(md_f)
    html = html_node.to_html()
    extract_title(md_f)
    
    #TODO Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.

    #TODO Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.



    

