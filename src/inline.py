from textnode import TextNode, TextType
import re

delimiters = {"**":TextType.BOLD,
              "*":TextType.ITALIC,
              "`":TextType.CODE,
              }
       
#test whether this one returns more than three-item list when given a TextNode with more delimiters
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if isinstance(old_nodes, list) == False:
        raise ValueError("old_nodes must be a list.")
    if delimiter not in delimiters.keys():
        raise ValueError("invalid delimiter.")
    new_nodes = []
    for node in old_nodes:
        for key in delimiters.keys():
            if key in node.text and key == delimiter:
                parted = node.text.partition(delimiter)
                new_nodes.append(TextNode(parted[0], text_type))

                parted2 = parted[2].partition(delimiter)
                new_nodes.append(TextNode(parted2[0], delimiters[delimiter]))
                if parted2[2] != "":
                    new_nodes.append(TextNode(parted2[2], text_type))
                break
        else:
            new_nodes.append(node)
    return(new_nodes)


# images
r"(!\[([^\[\]]*)\])(\(([^\(\)]*)\))"

# regular links
r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


#$h@w3r07her5-Wux1@-G0ng-Fu


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            # this function has to be applied before split_nodes_delimiter
            new_nodes.append(node)
            continue
        ptrn = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        arglist = re.split(ptrn, node.text)
        imagelist = extract_markdown_images(node.text)

        arglist = re.split(ptrn, node.text)
        
        i = 0

        while i < len(arglist):
            if i+1 < len(arglist) and (arglist[i], arglist[i+1]) in imagelist:
                new_nodes.append(TextNode(arglist[i], TextType.IMAGE, arglist[i+1]))
                i += 2
                continue
            elif arglist[i] != "":
                new_nodes.append(TextNode(arglist[i], TextType.NORMAL))
            i += 1
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            # this function has to be applied before split_nodes_delimiter
            new_nodes.append(node)
            continue

        ptrn = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

        arglist = re.split(ptrn, node.text)
        linklist = extract_markdown_links(node.text)

        arglist = re.split(ptrn, node.text)
        
        i = 0

        while i < len(arglist):
            if i+1 < len(arglist) and (arglist[i], arglist[i+1]) in linklist:
                new_nodes.append(TextNode(arglist[i], TextType.LINK, arglist[i+1]))
                i += 2
                continue
            elif arglist[i] != "":
                new_nodes.append(TextNode(arglist[i], TextType.NORMAL))
            i += 1
    return new_nodes

def text_to_text_nodes(text):
    '''convert raw md text into list of txtnodes'''

    # convert text to basic textnode
    btn = TextNode(text, TextType.NORMAL) 

    # plus split by imgs n links
    iltn = split_nodes_link(split_nodes_image([btn]))

    def sloop(l, d):
        # go through nodes in iltn and split txtnodes by delimiters
        fl = []
        for n in l:
            # split node into formated nodes
            sn = split_nodes_delimiter([n], d, n.text_type)
            # add each of them to the final list
            for i in sn:
                if i.text != "" and i.text_type !=TextType.IMAGE:
                    fl.append(i)

        return fl

    # sloop through all delimiters and return the [f]inal
    f = iltn
    for k in delimiters.keys():
        f = sloop(f,k)
    
    return f

               

    
    # example input:
    # This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)

    #  example output:
    # [
    # TextNode("This is ", TextType.TEXT),
    # TextNode("text", TextType.BOLD),
    # TextNode(" with an ", TextType.TEXT),
    # TextNode("italic", TextType.ITALIC),
    # TextNode(" word and a ", TextType.TEXT),
    # TextNode("code block", TextType.CODE),
    # TextNode(" and an ", TextType.TEXT),
    # TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    # TextNode(" and a ", TextType.TEXT),
    # TextNode("link", TextType.LINK, "https://boot.dev"),
    # ]

