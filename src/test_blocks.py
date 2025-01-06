import unittest
from blocks import *


class test_md2blocks(unittest.TestCase):
    def io(self):
        tr = '''# This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item'''
        
        tb = ["This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block", "* This is a list item", "* This is another list item'"]

        self.assertEqual(tb, markdown_to_blocks(tr))

class test_block2block_type(unittest.TestCase):
    def loop_correct_heading(self):
        suffix = " sometext"
        i = 1 
        block = ""
        while i < 7:

            block = i * "#" + suffix
            self.assertEqual(block_to_block_type(block), "heading")

    def test_too_much_hash_for_my_heading(self):
        self.assertNotEqual(block_to_block_type("####### suffix"), "heading")

    def test_no_space_heading(self):
        self.assertNotEqual(block_to_block_type("#suffix"), "heading")

    def test_code_correct_spaces(self):
        backticks = "```"
        space = " "
        cblock = r"```       ```"
        print(f"cblock {cblock}")
        self.assertEqual(block_to_block_type(cblock), "code")

    def test_code_only_srart_or_end(self):
        start = "```     "
        self.assertNotEqual(block_to_block_type(start), "code")
        end = "       ```"
        self.assertNotEqual(block_to_block_type(end), "code")

    def test_quote_correct_manylines(self):
        start = ">   \n"
        block = None
        for i in range (1,100):
            block = start * i 
            self.assertEqual(block_to_block_type(block), "quote")

    def test_quote_no_arrow(self):
        # no arrows at all
        block = "this is not a quote"
        self.assertNotEqual(block_to_block_type(block), "quote")
        # no arrow in the first line
        block0 = "this is not a quote \n>although it has an arrow"
        self.assertNotEqual(block_to_block_type(block0), "quote")

    def test_unordered_correct(self):
        # only hyphens
        h_list = "- something\n- for your body\n- your mind\n- and your soul"
        self.assertEqual(block_to_block_type(h_list), "unordered_list")
        # only asterisks
        a_list = "* a\n* b\n* c"
        self.assertEqual(block_to_block_type(a_list), "unordered_list")
        # mixed
        m_list = "* once\n- upon\n- a \n* time"
        self.assertEqual(block_to_block_type(m_list), "unordered_list")
    def test_unordered_wrong_lines(self):
        # wrong newline
        nl_list = "- it started well \n but it ended badly"
        self.assertNotEqual(block_to_block_type(nl_list), "unordered_list")
        
        # no -/* on the first line

        n1st = "i don't\n- know"
        self.assertNotEqual(block_to_block_type(n1st), "unordered_list")

        # not a list at all
        bs_list = "this is \n not a list"
        self.assertNotEqual(block_to_block_type(bs_list), "unordered_list")

    def test_ordered_correct(self):
        #starting with 0
        z_list = "0. this \n1. is \n2. a \n3. realm \n4. of \n5. order"
        self.assertEqual(block_to_block_type(z_list), "ordered_list")
        #starting with 1
        #starting with 49

class test_format_block_txt(unittest.TestCase):
    def test_heading_strip(self):
        h6 = "###### foo"
        fh6 = format_block_txt(h6, "heading")
        self.assertEqual(fh6, "foo")

        h1 = "# baz"
        fh1 = format_block_txt(h1, "heading")
        self.assertEqual(fh1, "baz")

        h_more = "# ## "
        fh_more = format_block_txt(h_more, "heading")
        self.assertEqual(fh_more, "## ")

        h2much = "########### foobar"
        fh2much = format_block_txt(h2much, "paragraph")
        self.assertNotEqual(fh2much, "foobar")
        self.assertEqual(fh2much, h2much)

        nospace = "#foobarbaz"
        fnospace = format_block_txt(nospace, "paragraph")
        self.assertEqual = (fnospace, nospace)

    def test_code_strip(self):
        c = "```foo```"
        fc = format_block_txt(c, "code")
        self.assertEqual(fc, "foo")

    
    def test_notquote(self):
        nq = "foo\n>bar"
        fnq = format_block_txt(nq, "paragraph")
        self.assertEqual(nq, fnq)

    def test_proper_quote(self):
        pq = ">foo\n>bar"
        fpq = format_block_txt(pq, "quote")
        self.assertEqual(fpq,"foo\nbar")

    def test_unordered_list(self):
        ul = "- foo\n- bar"
        ful = format_block_txt(ul, "unordered_list")
        self.assertEqual(ful, "foo\nbar")

        ul1 = "* foo\n* bar"
        ful1 = format_block_txt(ul1, "unordered_list")
        self.assertEqual(ful1, "foo\nbar")

    def test_not_ul(self):
        nl = "foo\n* bar"
        fnl = format_block_txt(nl, "paragraph")
        self.assertNotEqual(fnl, "foo\nbar")

        l = "* foo\n* bar"
        fl = format_block_txt(l, "unordered_list")
        self.assertNotEqual(fnl,l)


class test_markdown2htmlnode(unittest.TestCase):
    pass


class test_makehnode(unittest.TestCase):
    def test_noinlinefmt(self):
        #test_cnode = ParentNode(tag="pre", children=[test_hcode])
        #cnode = make_hnode("code", "code", "somecode")
        #self.assertEqual(repr(cnode), repr(test_cnode))

        test_qnode = ParentNode(tag="blockquote", children=[LeafNode(tag=None, value="whosaid")])
        qnode = make_hnode("quote", "blockquote", btext="whosaid")
        self.assertEqual(repr(qnode), repr(test_qnode))

        test_olli = [LeafNode(tag="li", value="first item"), LeafNode(tag="li", value="second item")]
        test_olnode = ParentNode(tag="ul", children=test_olli)
        olnode = make_hnode("unordered_list", "ul", "first item\nsecond item")
        print("\\\\\\" + "test: " + repr(test_olnode) + "\n")
        print("\\\\\\" + "actual: " + repr(olnode) + "\n")
        self.assertEqual(repr(olnode), repr(test_olnode))

    def test_headingfmt(self):
        # normal
        test_hdnode_n = ParentNode(tag="h1", children=[LeafNode(tag=None,value="title")])
        hdnode_n = make_hnode("heading", "h1", btext="title")
        self.assertEqual(repr(hdnode_n), repr(test_hdnode_n))

    def test_headingfmt_bold(self):
        #bold
        test_hdnode_b = ParentNode(tag="h1", children=[LeafNode(tag="b",value="title")])
        hdnode_b = make_hnode("heading", "h1", btext="**title**")
        self.assertEqual(repr(hdnode_b), repr(test_hdnode_b))
    
    def test_headingfmt_italic(self):
        test_hdnode_i = ParentNode(tag="h1", children=[LeafNode(tag="i",value="title")])
        hdnode_i = make_hnode("heading", "h1", btext="*title*")
        self.assertEqual(repr(hdnode_i), repr(test_hdnode_i))

    def test_headingfmt_code(self):
        test_hdnode_c = ParentNode(tag="h1", children=[LeafNode(tag="code",value="title")])
        hdnode_c = make_hnode("heading", "h1", btext="`title`")
        self.assertEqual(repr(hdnode_c), repr(test_hdnode_c))

    
    def test_headingfmt_link(self):
        test_hdnode_l = ParentNode(tag="h1", children=[LeafNode(tag="a",value="title", props="href")])
        hdnode_l = make_hnode("heading", "h1", btext="[title](url)")
        self.assertEqual(repr(hdnode_l), repr(test_hdnode_l))

    def test_headingfmt_image(self):
        test_hdnode_l = ParentNode(tag="h1", children=[LeafNode(tag="a",value="title", props="href")])
        hdnode_l = make_hnode("heading", "h1", btext="![alttext])[https://www.example.com/image.png]")
        self.assertEqual(repr(hdnode_l), repr(test_hdnode_l))

    def test_quotefmt(self):
        pass

    def test_listfmt(self):
        pass
        

class test_text2children(unittest.TestCase):
    def test_txt2linknode(self):
        txt = "[alttext](https://www.example.com)"


