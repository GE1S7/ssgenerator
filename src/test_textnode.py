import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        lumbago_node = TextNode("My lumbago is killing me", TextType.BOLD, "https://achyback.com")
        fine_node = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(lumbago_node, fine_node)

    def test_noneurl(self):
        nourl_node = TextNode("This is a txt node with no url", TextType.NORMAL)
        self.assertIsNone(nourl_node.url)

    def test_withurl(self):
        withurl_node = TextNode("This is a txt node with url", TextType.NORMAL, "https://zal.pl")
        self.assertIsNotNone(withurl_node.url)

    def test_wrongtype(self):
        wrongtype_node = TextNode("This txt has wrong type", "WRONG")
        self.assertNotIn(wrongtype_node.url, TextType) 

class TxtNode2HtmlNode(unittest.TestCase):
    def test_text(self):
        pure_text_node = TextNode("asdfgh", TextType.NORMAL)
        conv_node = pure_text_node.text_node_to_html_node()

        self.assertIsNone(conv_node.tag)
        self.assertIsNone(conv_node.props)

        self.assertEqual("asdfgh", conv_node.value)

    def test_bold(self):
        bold_node = TextNode("big boi", TextType.BOLD)
        conv_node = bold_node.text_node_to_html_node()

        self.assertEqual(conv_node.tag, "b")


    def test_italic(self):

        italic_node = TextNode("coca-cola", TextType.ITALIC)
        conv_node = italic_node.text_node_to_html_node()

        self.assertEqual(conv_node.tag, "i")

    def test_text_code(self):
        code_node = TextNode("print(Hello, world)", TextType.CODE)
        conv_node = code_node.text_node_to_html_node()

        self.assertEqual(conv_node.tag, "code")


    def test_test_type_link(self):
        link_node = TextNode("click this!", TextType.LINK, "www.example.com")
        conv_node = link_node.text_node_to_html_node()

        self.assertEqual(conv_node.tag, "a")
        self.assertEqual(conv_node.props, {"href":"www.example.com"})


    def test_type_image(self):
        image_node = TextNode("description", TextType.IMAGE, "www.example.com/img.png")
        conv_node = image_node.text_node_to_html_node()
        self.assertEqual(conv_node.tag, "img")
        self.assertEqual(conv_node.props, {'src':"www.example.com/img.png", 'alt':"description"})

        image_node0 = TextNode("alttext", TextType.IMAGE, "https://www.example.com/image.png")
        test_html_node0 = LeafNode(tag="img",value="", props={"src":"https://www.example.com/image.png","alt":"alttext"})
        conv_node0 = image_node0.text_node_to_html_node()
        print(f"conv_node0    =    {conv_node0}\ntest_html_node0    =    {test_html_node0}")
        self.assertEqual(conv_node0, test_html_node0)


        
class TestHTMLNode(unittest.TestCase):
    def test_eq_noatr(self):
        n1 = HTMLNode()
        n2 = HTMLNode()
        self.assertEqual(n1, n2)

    def test_eq_atr(self):
        no1 = HTMLNode("a", "b", "c", "d")
        no2 = HTMLNode("a", "b", "c", "d")
        self.assertEqual(no1, no2)
        

    def test_noteq_atr(self):   
        nod1 = HTMLNode("sdfl", "asdf", "asdf", "oiwef")
        nod2 = HTMLNode("and now", "for something", "completely", "different")
        self.assertNotEqual(nod1, nod2)

    def test_repr(self):
        hn = HTMLNode("1", "2", "3", "4")
        tp = f"HTMLNode({"1"}, {"2"}, {"3"}, {"4"})"
        self.assertEqual(hn.__repr__(), tp)

    def test_props2html(self):
       pass 


    

        

if __name__ == "__main__":
    unittest.main()
