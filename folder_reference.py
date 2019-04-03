'Reference for what artists etc. should exist per (sub)folder'

import os

RAW_REFERENCE_FILE = 'raw_reference.md'

# TODO: make ref object into a class with its own checker functions to e.g. return the category of something (or None if nothing found)
def setup_folder_reference():
    ref = {
        'folders': {},
        'labels': {}
    }

    opened_ref_file = open(os.path.join(os.getcwd(), RAW_REFERENCE_FILE))
    ref_lines = opened_ref_file.readlines()
    opened_ref_file.close()

    sub_ref: str    = None
    collection: str = None
    criterion: str  = None

    for line in ref_lines:
        if sub_ref:
            if line.startswith('<!--'):
                sub_ref    = None
                collection = None
                criterion  = None
                continue
            
            if line.startswith('#'):
                criterion = line.split('###')[-1].strip()
                ref[sub_ref][collection][criterion] = []
            elif line.strip().__len__ != 0 and criterion:
                ref[sub_ref][collection][criterion].append(line)
            
        else:
            if line.startswith('###'):
                sub_ref = 'labels'
            elif line.startswith('##'):
                sub_ref = 'folders'

            if sub_ref:
                collection = line.split('#')[-1].strip()
                ref[sub_ref][collection] = {}
        
    return ref

FOLDER_REFERENCE = setup_folder_reference()


'''
Things to look for:
- colletion name
- artist name
- song title

Further tags to attach per song:
- easy:     has a max diff of e.g. 7
- effects:  has cool scrolling effects et
- like:     definitely approved by me (manual per song or sth)
- video:    (has background video)
- meh:      (not much fun or sth, manual)

Stuff:
- so the 'individual songs' should of course take precedence over if something is in 'artists'


'''
