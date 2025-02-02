from textnode import *
from copy import copy_dir
from website import  generate_page

print('hello world')

def main():
    static ="/home/kacper/boot.dev/ssgenerator/static"
    public ="/home/kacper/boot.dev/ssgenerator/public"
    copy_dir(static,public)
    generate_page("/home/kacper/boot.dev/ssgenerator/content/index.md", "/home/kacper/boot.dev/ssgenerator/template.html", "/home/kacper/boot.dev/ssgenerator/public/index.html")
    

main()


