'Script for arranging OpenITG collection'

import os
from typing import List

from folder_reference import FOLDER_REFERENCE as FR

print()

SONGS_DIR = r'F:\voorSnelkoppelingen\H\OpenITG\Songs'
NEW_SONGS_DIR = r'F:\voorSnelkoppelingen\H\OpenITG\SongsOrganised'

def format_title(previous_title: str, labels: List[str]):
    return f'<{", ".join(labels)}> {previous_title}'
    


def main():
    
    if not os.path.exists(SONGS_DIR):
        raise Exception('Path doesn\'t exist')
    
    pack_folders: List[str] = os.listdir(SONGS_DIR)

    for i, pack in enumerate(pack_folders):
        if i > 3:
            break

        col_path = os.path.join(SONGS_DIR, pack)
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

            artist: str
            title: str

            opened_sm_file = open(os.path.join(song_path, sm_file))
            for j, line in enumerate(opened_sm_file):
                if line.startswith('#NOTES') or j > 100:
                    break
                elif line.startswith('#TITLE:'):
                    title = line.split(':')[-1].strip().split(';')[0]
                elif line.startswith('#ARTIST:'):
                    artist = line.split(':')[-1].strip().split(';')[0]

            opened_sm_file.close()

            try:
                migration_info = FR.match_song({
                    'artist': artist, 'title': title, 'pack': pack
                })
            # TODO: throw this if it's not my own exception
            except Exception as e:
                if str(e) == 'No match':
                    continue
                else:
                    raise e
                

            print(migration_info)

            return
            # hier nog een hoop formatting doen enzo en dan daadwerkelijk de migraties plaats laten vinden

            # print(song_path)
            # print(format_title(title, migration_info['labels']))

            






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
