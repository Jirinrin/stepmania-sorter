'Script for arranging OpenITG collection'

import os
from typing import List

from folder_reference import FOLDER_REFERENCE as FR

print()

SONGS_DIR = r'F:\voorSnelkoppelingen\H\OpenITG\Songs'
    

def main():
    
    if not os.path.exists(SONGS_DIR):
        raise Exception('Path doesn\'t exist')
    
    collection_folders: List[str] = os.listdir(SONGS_DIR)

    for i, col in enumerate(collection_folders):
        if i > 3:
            break

        col_path = os.path.join(SONGS_DIR, col)
        song_folders = os.listdir(col_path)


        for song in song_folders:
            song_path = os.path.join(col_path, song)

            if os.path.isfile(song_path):
                continue

            files = os.listdir(song_path)
            # TODO: test if you can just get filter()[0]
            sm_file = next(filter(lambda x: x.split('.')[-1] == 'sm', files), None)

            if not sm_file:
                continue

            opened_sm_file = open(os.path.join(song_path, sm_file))
            for j, line in enumerate(opened_sm_file):
                if line.startswith('#NOTES') or j > 100:
                    break
                elif line.startswith('#ARTIST'):
                    artist: str = line.split(':')[-1]

            opened_sm_file.close()






main()

print()


'''

Functionality:
- Move to right location or sth
- Check if it has interesting tricks
- Do something if it only has a certain max difficulty
- Group stuff by 'something' (?)
- Rename folders to make sense or sth
- Give stuff extra tags

'''
