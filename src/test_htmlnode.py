import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
       node = HTMLNode(props={"href": "https://www.google.com"})
       convref = ' href="https://www.google.com"'
       self.assertEqual(node.props_to_html(), convref)

    
class Test_LeafNode(unittest.TestCase):
    def test_conv_equal(self):
        ln1 = LeafNode("p", "This is a paragraph of text.", None)
        ln1_test = "<p>This is a paragraph of text.</p>"
        self.assertEqual(ln1.to_html(), ln1_test)

        ln2 = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        ln2_test = '<a href="https://www.google.com">Click me!</a>'
        self.assertIsNotNone(ln2.props)
        self.assertEqual(ln2.to_html(), ln2_test)
        
    def test_tag(self):
        ln1 = LeafNode(None,"something", None)
        self.assertIsNone(ln1.tag)

        ln2 = LeafNode("p", "else", None)
        self.assertIsNotNone(ln2.tag)

    def test_props(self):
        ln1 = LeafNode("span", "text", {'style':'color=rgb(0,0,0)'}) 
        self.assertIsNotNone(ln1.props)
        
        ln2 = LeafNode(None, "text", None)
        self.assertIsNone(ln2.props)

class Test_ParentNode(unittest.TestCase):
    def tes_value_errors(self):
        pn_tag= ParentNode(None, [], {"href":"https://www.google.com"})
        assertRaises(ValueError,pn_tag.to_html)
        
        pn_children('p', None, {"href":"https://www.google.com"})
        assertRaises(ValueError,pn_children.to_html)

    def test_props_optional(self):
        pn_propsless = ParentNode('p', [])
        self.assertIsNone(pn_propsless.props)
        pn_withprops = ParentNode('p',[],props={"href":"https://www.google.com"})
        self.assertIsNotNone(pn_withprops.props)

    def test_to_html(self):
        n1 = ParentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),],)

        n1_proper_conv = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        
        self.assertEqual(n1.to_html(), n1_proper_conv)


if __name__ == "__main__":
    unittest.main
