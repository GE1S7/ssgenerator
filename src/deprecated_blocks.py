def markdown_to_blocks(markdown):
    '''Turns continous text into a blocklist'''
    markdown.split()
    blist = markdown.split("\n\n")
    # TODO: remove empty blocks due to excessive newlines
    return blist


print(markdown_to_blocks('''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item'''))
