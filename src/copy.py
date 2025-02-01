import os
import shutil
def copy_dir(src, dst):
    '''recursively move files from source dir to dest dir'''
    # no such src path
    if os.path.lexists(src) == False:
        raise FileNotFoundError("Source directory not found.")

    # clean & create dst
    if os.path.lexists(dst) == True:
        shutil.rmtree(dst)

    os.mkdir(dst)

    # list src entry names
    names = os.listdir(src)

    for name in names:
        src_entry = os.path.join(src, name)
        dst_entry = os.path.join(dst, name)
        
        # copy files
        if os.path.isfile(src_entry):
            shutil.copy(src_entry, dst_entry)

        else:
        # copy folders recursively
            copy_dir(src_entry, dst_entry)
