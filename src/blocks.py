import re
from htmlnode import HTMLNode
from inline import text_to_text_nodes

def markdown_to_blocks(markdown):
    # take raw md string
    # split the string into blocks by "\n\n" (empty newline)
    # strip leading&trailing whitespaces from each block
    # remove any "empty" blocks due to excessive newlines

    blocks = []
    for i in list(map(strip, markdown.split("\n\n"))):
        if i == "\n":
            continue
        blocks.append(i)

    return blocks

def block_to_block_type(block):
    if re.match(r"^(#{1,6} )", block) != None:
        return "heading"

    elif re.match("```", block) != None and re.search(r"```$", block):
        return "code" 

    elif re.match(">", block) != None:
        if re.search("\n(?!>)", block) != None:
            return "quote"
        
    elif re.match(r"^([\*\-] )", block):
        if re.search(r"\n(?![\*\-])", block) == None:
            return "unordered_list"
        
    elif re.match(r"[0-9]*\. ", block):
        if re.search(r"\n[0-9]*\. ", block) != None:
            line_starters = re.findall(r"(?:\n|\A)([0-9]*)(?=\. )", block) 
            print(f"hi! these are your linestarters: {line_starters}")
            i = 1
            ordered = True
            
            while i <= len(line_starters):
                print(int(i))
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
        htag = mdtype2htmltag(btype)

        btext = format_block_txt(block, btype)

        hnode = make_hnode(btype, htag, btext)

        allch.append(hnode)

        # making an hnode can be a separate function itself. It could use text_to_children too.

        if btype == "code":
            hcode = LeafNode(tag=htag, value=btext)
            hpre = ParentNode(tag="pre", children=[hcode])
            allnode.children.append(hpre)

        if btype == "heading":
            # no fancy stuff
            pass

        if btype == "quote":
            # no fancy stuff
            pass

        if btype == "unordered_list" or btype == "ordered_list":
            bli = btext.split("\n")
            hli = []
            for line in bli:
                hline_ch = text_to_children(line)
                hli.append(hline_ch)
            hall_li = ParentNode(tag=htag, children=hli)
            allnode.append(hall_li)
            continue


        chnodes = text_to_children(btext, btype)
        
        hnode = ParentNode(tag=htag, children=chnodes)

    allnode = ParentNode("div", allch)


def mdtype2htmltag(mdtype):
    typetag = {"heading":"h", #TODO: headings are numbered: <h1>-<h6> resp. md #
               "code":"code", #TODO: code blocks should be nested insida a <pre> tag
               "quote":"blockquote",
               "unordered_list":"ul", #TODO: each list item is surrounded with <li> tag
               "ordered_list":"ol",
               "paragraph":"p"
               }
    if mdtype in typetag.keys():

        if mdtype == "heading":
            # count hashes
            hn = 0
            for i in mdtype:
                if  "#":
                    hn += 1
                else:
                    break
            if hn == 0:
                raise ValueError("Not a heading")
            htype = f"<h{hn}>"

        else:
            htype = typetag[mdtype]
        return htype

    else:
        raise ValueError("Unrecognized markdown type")

#TODO should "#" after the "# "  be treated as belonging to heading's txt? At least in obsidian this is the case. 
#TODO no mdformatting wihtin code block (vide obsidian).

def format_block_txt(text, mdtype):
    # TODO: \n \A should not be matched, only what comes after them
    if mdtype == "heading":
        text = re.sub(r"\A(#{1,6} )", "", text) 

    elif mdtype == "code":
        text = text.removeprefix("```")
        text = text.removesuffix("```")
        
    elif mdtype == "quote":
        text = re.sub(r"^>", "", text)
        text = re.sub(r"\n>", "\n", text)

    elif mdtype == "unordered_list":
        text = re.sub("^([\*\-] )", "", text)
        text = text.replace ("\n* ", "\n")
        text = text.replace ("\n- ", "\n")

    elif mdtype == "ordered_list": 
        text = re.sub(r"\A([0-9]*)(?=\. )", "", text)
        text = re.sub(r"\n([0-9]*)(?=\. )", "\n", text)

    return text


def make_hnode(btype, htag, btext)
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
            qtnode = ParentNode(tag=htag, children=chnodes)
            return qtnode

        if btype == "unordered_list" or btype == "ordered_list":
            bli = btext.split("\n")
            hli = []
            for line in bli:
                #TODO: split lines into nodes
                hline_ch = text_to_children(line)
                hli.append(hline_ch)
            hall_li = ParentNode(tag=htag, children=hli)
            return(hall_li)


def text_to_children(text, mdtype):
    # takes a block and it's markdown type and returns a list of html child nodes 
    chn = text_to_text_nodes(text)
    return chn
