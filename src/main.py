from textnode import *
from copy import copy_dir

print('hello world')

def main():
    static ="/home/kacper/boot.dev/ssgenerator/static"
    public ="/home/kacper/boot.dev/ssgenerator/public"
    copy_dir(static,public)

main()


