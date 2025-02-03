from textnode import *
from copy import copy_dir
from website import generate_pages_recursive

def main():
    static ="/home/kacper/boot.dev/ssgenerator/static"
    public ="/home/kacper/boot.dev/ssgenerator/public"
    copy_dir(static,public)
    print("directory copied")
    generate_pages_recursive("/home/kacper/boot.dev/ssgenerator/content/", "/home/kacper/boot.dev/ssgenerator/template.html", "/home/kacper/boot.dev/ssgenerator/public/")
    

main()


