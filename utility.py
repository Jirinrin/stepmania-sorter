'Utility functions for other modules to use'

from difflib import SequenceMatcher
import shutil
from os import path
from re import sub

def similar(string_1: str, string_2: str, s2_subtitle: str = ''):
    string1 = string_1.lower()
    string2 = string_2.lower()
    # print(string_1, string_2)
    if '<in>' in string1:
        string1 =  string1.split('<in>')[1]
        if string1 in string2 + s2_subtitle.lower():
            return 1
    # make thing for <sub> so that it checks with subtitle
    # make thing so that you can specify what artist belongs to a track in case of a homonymous track
    
    return SequenceMatcher(None, string1, string2).ratio()

def safe_move(file_path: str, out_dir: str, dst = None):
    '''Safely move a file to the specified directory. If a file with the same name already 
    exists, the copied file name is altered to preserve both.

    :param str file_path: Path to the file to move.
    :param str out_dir: Directory to move the file into.
    :param str dst: New name for the copied file. If None, use the name of the original
        file.
    '''
    name = dst or path.basename(file_path)
    if (not path.exists(path.join(out_dir, name))) or file_path == path.join(out_dir, name):
        shutil.move(file_path, path.join(out_dir, name))
    else:
        base, extension = path.splitext(name)
        i = 1
        while path.exists(path.join(out_dir, '{}_{}{}'.format(base, i, extension))):
            i += 1
        shutil.move(file_path, path.join(out_dir, '{}_{}{}'.format(base, i, extension)))

def format_for_windows(name: str) -> str:
    return sub(r'[<>:"/\|?*]', '-', name)
