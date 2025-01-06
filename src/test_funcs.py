import unittest
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_nodes
from textnode import TextNode, TextType
import re


class TestSplitNodesDelimiter(unittest.TestCase): 
    def test_input_type(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.NORMAL)
        compare = [TextNode("This is text with a ", TextType.NORMAL), TextNode("code block", TextType.CODE), TextNode(" word", TextType.NORMAL)]
        self.assertEqual(new_nodes, compare)

        node0 = TextNode("This is text with a *italicised* word", TextType.NORMAL)
        new_nodes0 = split_nodes_delimiter([node0], "*", TextType.NORMAL)
        compare0 = [TextNode ("This is text with a ", TextType.NORMAL), TextNode("italicised", TextType.ITALIC), TextNode(" word", TextType.NORMAL)] 
        self.assertEqual(new_nodes0, compare0)

        node1 = TextNode("This is text with a **bold** word", TextType.NORMAL)
        new_nodes1 = split_nodes_delimiter([node1], "**", TextType.NORMAL)
        compare1 = [TextNode ("This is text with a ", TextType.NORMAL), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.NORMAL)] 
        self.assertEqual(new_nodes1, compare1)



class TestExtractMarkdownImages(unittest.TestCase):
    def test_io(self):
        i1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        o1 = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        func_o1 = extract_markdown_images(i1)
        self.assertEqual(o1,func_o1)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_io(self):
        i1 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        o1 = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        func_o1 = extract_markdown_links(i1)
        self.assertEqual(o1,func_o1)

class TestSplitNodesImage(unittest.TestCase):
    def test_txt_img(self):
        #txt-img
        n = TextNode("This is text with an image ![dog](https://www.imgs.com/shiba_inu.png)", TextType.NORMAL)
        tn = [TextNode("This is text with an image ", TextType.NORMAL), TextNode("dog", TextType.IMAGE, "https://www.imgs.com/shiba_inu.png")]
        sn = split_nodes_image([n])
        self.assertEqual(tn, sn)

    def test_img_txt(self):
        n = TextNode("![dog](https://www.imgs.com/shiba_inu.png) this is text with an image", TextType.NORMAL)
        tn = [TextNode("dog", TextType.IMAGE, "https://www.imgs.com/shiba_inu.png"), TextNode(" this is text with an image", TextType.NORMAL)]
        sn = split_nodes_image([n])
        self.assertEqual(tn, sn)

    def test_no_img(self):
        n = TextNode("I'm just an everyday regular normal motherfucker", TextType.NORMAL)
        tn = [TextNode("I'm just an everyday regular normal motherfucker", TextType.NORMAL)]
        sn = split_nodes_image([n])
        self.assertEqual(tn, sn)

    def test_only_img(self):
        n = TextNode("![obrazek](https://www.grafika.pl/picture.jpg)", TextType.NORMAL)
        tn = [TextNode("obrazek", TextType.IMAGE, "https://www.grafika.pl/picture.jpg")]
        sn = split_nodes_image([n])
        self.assertEqual(tn, sn)
   

class TestSplitNodesLink(unittest.TestCase):
    def test_io(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        test_nodes = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
         ]

        splt_nd = split_nodes_link([node])

        self.assertEqual(test_nodes, splt_nd)

    def test_no_link(self):
        tn = [TextNode("This is normal text", TextType.NORMAL)]
        on = split_nodes_link([TextNode("This is normal text", TextType.NORMAL)])
        self.assertEqual(tn,on)
        on0 = split_nodes_image(tn)
        self.assertEqual(tn, on0)

    def test_only_link(self):
        tn = [TextNode("[description](https://www.example.com", TextType.NORMAL)]
        on = split_nodes_link(tn)

    def test_nonurltail(self):
        node = TextNode(
                "I would show you something like this [webpage](https://www.page.com) or like this [site](https://www.website.com) but instead I will tell you this...",TextType.NORMAL)

        test_nodes = [
            TextNode("I would show you something like this ", TextType.NORMAL),
            TextNode("webpage", TextType.LINK, "https://www.page.com"),
            TextNode(" or like this ", TextType.NORMAL),
            TextNode("site", TextType.LINK, "https://www.website.com"),
            TextNode(" but instead I will tell you this...", TextType.NORMAL),
            ]
        splt_nd = split_nodes_link([node])

        self.assertEqual(test_nodes, splt_nd)

class TestTextToTextNodes(unittest.TestCase):
    def test_io_mix(self):
        i =  "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        o = [TextNode("This is ", TextType.NORMAL),
             TextNode("text", TextType.BOLD),
             TextNode(" with an ", TextType.NORMAL),
             TextNode("italic", TextType.ITALIC),
             TextNode(" word and a ", TextType.NORMAL),
             TextNode("code block", TextType.CODE),
             TextNode(" and an ", TextType.NORMAL),
             TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
             TextNode(" and a ", TextType.NORMAL),
             TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        i2o = text_to_text_nodes(i)

        self.assertEqual(o, i2o)

    def test_io_single(self):
        i = "This is text"
        o = [TextNode("This is text", TextType.NORMAL)]
        i2o = text_to_text_nodes(i)
        self.assertEqual(o,i2o)

        i0 = "This is *italic*"
        o0 = [TextNode("This is ", TextType.NORMAL), TextNode("italic", TextType.ITALIC)]
        i2o0 = text_to_text_nodes(i0)
        self.assertEqual(o0,i2o0)

        i1 = "This is **bold**"
        o1 = [TextNode("This is ", TextType.NORMAL), TextNode("bold", TextType.BOLD)]
        i2o1 = text_to_text_nodes(i1)
        self.assertEqual(o1,i2o1)

        i2 = "This is `code`"
        o2 = [TextNode("This is ", TextType.NORMAL), TextNode("code", TextType.CODE)]
        i2o2 = text_to_text_nodes(i2)
        self.assertEqual(o2,i2o2)

        i3 = "![link to image](https://i.imgur.com/fJRm4Vk.jpeg)"
        o3 = [TextNode("link to image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
        i2o3 = text_to_text_nodes(i3)
        self.assertEqual(o3,i2o3)

        i4 = "[regular link](https://i.imgur.com/fJRm4Vk.jpeg)"
        o4 = [TextNode("regular link", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg")]
        i2o4 = text_to_text_nodes(i4)
        self.assertEqual(o4,i2o4)


