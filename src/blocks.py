import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline import text_to_text_nodes

def markdown_to_blocks(markdown):
    # take raw md string
    # split the string into blocks by "\n\n" (empty newline)
    # strip leading&trailing whitespaces from each block
    # remove any "empty" blocks due to excessive newlines

    blocks = []
    for i in  markdown.split("\n\n"):
        i.strip()
        if i == "\n":
            continue
        blocks.append(i)

    print(blocks)
    return blocks

def block_to_block_type(block):
    if re.match(r"^(#{1,6} )", block) != None:
        return "heading"

    elif re.match("```", block) != None and re.search(r"```$", block):
        return "code" 

    elif re.match("^(?!>)", block, re.MULTILINE) == None:
        #TODO something's not right here
        #print(block)
        #if re.search(r"\n(?!>)", block) != None:
        return "quote"
        
    elif re.match(r"^([\*\-] )", block):
        if re.search(r"\n(?![\*\-])", block) == None:
            return "unordered_list"
        
    elif re.match(r"[0-9]*\. ", block):
        if re.search(r"\n[0-9]*\. ", block) != None:
            line_starters = re.findall(r"(?:\n|\A)([0-9]*)(?=\. )", block) 
            i = 1
            ordered = True
            
            while i <= len(line_starters):
                if int(i) == int(i-1) + 1:
                    ordered = True
                else:
                    ordered = False
                i += 1

            if ordered == True:
                return "ordered_list"
                

    else:
        return "paragraph"

def markdown_to_html_node(markdown):
    ''' Convert a full markdown document 
    into a single parent HTMLNode '''
    allch = []
    
    bs = markdown_to_blocks(markdown)

    for block in bs:
        btype = block_to_block_type(block)
        htag = mdtype2htmltag(btype, block)

        btext = format_block_txt(block, btype)
        print(f"btext: {btext}")

        hnode = make_hnode(btype, htag, btext)

        allch.append(hnode)

    allnode = ParentNode("div", allch)
    return allnode


def mdtype2htmltag(mdtype, block):
    typetag = {"heading":"h",
               "code":"code",
               "quote":"blockquote",
               "unordered_list":"ul",
               "ordered_list":"ol",
               "paragraph":"p"
               }
    if mdtype in typetag.keys():

        if mdtype == "heading":
            # count hashes
            hn = 0
            #TODO it shouldn't count characters in text not in type...
            for i in block:
                if  i == "#":
                    hn += 1
                else:
                    break
            if hn == 0:
                raise ValueError("Not a heading")
            htype = f"h{hn}"

        else:
            htype = typetag[mdtype]
        return htype

    else:
        print(f"mdtype:{mdtype}\nblock:{block}")
        raise ValueError("Unrecognized markdown type")

def format_block_txt(text, mdtype):
    print(f"mdtype: {mdtype}, text: {text}")
    if mdtype == "heading":
        text = re.sub(r"\A(#{1,6} )", "", text) 

    elif mdtype == "code":
        text = re.sub(r"^```|```$", "", text)
        
    elif mdtype == "quote":
        text = re.sub(r"^>", "", text)
        text = re.sub(r"\n>", "\n", text)

    elif mdtype == "unordered_list":
        text = re.sub(r"^([\*\-] )", "", text)
        text = text.replace ("\n* ", "\n")
        text = text.replace ("\n- ", "\n")

    elif mdtype == "ordered_list": 
        text = re.sub(r"\A([0-9]*). ", "", text)
        text = re.sub(r"\n([0-9]*). ", "\n", text)

    return text

def make_hnode(btype, htag, btext):
    '''turn text of given mdtype to htmlnode with a given tag'''
    print(f"btext: {btext}")
    if btype == "code":
        # no text2children
        hcode = LeafNode(tag=htag, value=btext)
        hpre = ParentNode(tag="pre", children=[hcode])
        return hpre

    if btype == "heading":
        chnodes =  text_to_children(btext)
        hdnode = ParentNode(tag=htag, children=chnodes)
        return hdnode

    if btype == "quote":
        chnodes = text_to_children(btext)
        print(f"quote raw text: {btext}")
        print(f"quotetxt to children:   {chnodes}")
        qtnode = ParentNode(tag=htag, children=chnodes)
        return qtnode

    if btype == "unordered_list" or btype == "ordered_list":
        bli = btext.split("\n")
        print(bli)
        hli = []
        for line in bli:
            hline_ch = text_to_children(line, li=True)
            hli.append(hline_ch)
        hall_li = ParentNode(tag=htag, children=hli)
        return hall_li

    if btype == "paragraph":
        chnodes = text_to_children(btext)
        pnode = ParentNode(tag=htag, children=chnodes)
        return pnode

def text_to_children(text, li=False):
    '''takes a block and returns a list of html child nodes'''

    print(f"text: {text}")


    # convert text into a list of textnodes
    chn_txt = text_to_text_nodes(text)
    print(f"chn_text: {chn_txt}")
    
    # convert text nodes in the list into html nodes
    chn_html = []
    for i in chn_txt:
        child = i.text_node_to_html_node()
        # if li == True:
        #    child.tag = "li"
        #    return child
        chn_html.append(child)

    
    print(f"chn {chn_html}")
    if li == True:
        return ParentNode(tag="li",children=chn_html)
    return chn_html
