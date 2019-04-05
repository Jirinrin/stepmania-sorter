'Script for arranging OpenITG collection'

import os
from typing import List

from utility import safe_move
from folder_reference import FOLDER_REFERENCE as FR

print()

SONGS_DIR = r'F:\voorSnelkoppelingen\H\OpenITG\Songs'
# NEW_SONGS_DIR = r'F:\voorSnelkoppelingen\H\OpenITG\SongsOrganised'

def format_title(raw_previous_title: str, labels: List[str], artist: str = None):
    # als previous title al labels heeft snij dat deel dan eerst weg
    previous_title = raw_previous_title
    if raw_previous_title.startswith('<') and '>' in raw_previous_title:
        previous_title = raw_previous_title.split('>')[1]

    return f' { artist + " - " if artist else "<" + ", ".join(labels) + ">" } {previous_title}'
    


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
            title_line: int

            sm_file = os.path.join(song_path, sm_file)
            opened_sm_file = open(sm_file)

            for j, line in enumerate(opened_sm_file):
                if line.startswith('#NOTES') or j > 100:
                    break
                elif line.startswith('#TITLE:'):
                    title = line.split(':')[-1].strip().split(';')[0]
                    title_line = j
                elif line.startswith('#ARTIST:'):
                    artist = line.split(':')[-1].strip().split(';')[0]

            

            try:
                migration_info = FR.match_song({
                    'artist': artist, 'title': title, 'pack': pack
                })
                print(migration_info, artist, title, pack)

                new_title = format_title(title, migration_info['labels'])
                new_folder_name = format_title(title, migration_info['labels'], artist)

                # also write it in the file

                safe_move(
                    os.path.join(SONGS_DIR, pack, song), 
                    os.path.join(SONGS_DIR, '__' + migration_info['collection'] + '__'),
                    new_folder_name
                )

                # TODO: Could do this with temporary copy or sth
                lines = opened_sm_file.read().splitlines()
                lines[title_line] = f'#TITLE:{new_title};'
                opened_sm_file.close()
                writing_sm_file = open(sm_file,'w')
                writing_sm_file.write('\n'.join(lines))
                writing_sm_file.close()
            # TODO: throw this if it's not my own exception
            except Exception as e:
                if str(e) == 'No match':
                    continue
                else:
                    raise e
                
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


pythonding moet ook kunnen: 
collections opsplitsen als grootte over bepaalde threshold 
bijv (1), (2) appenden als titel al te vinden in een collection 
slash eigenlijk vooral bij mapnaam als Windowsoverschrijving niet lukt 

Ook gwn dat het dus voor de collecties (_KPOP_) enzo heen moet gaan en evt renamen slash dus verplaatsen ALS het naar een andere plek moet obv nieuwe analyse 

en nog label voor bijv boven bepaalde bpm, slash als bijv hele nare range, of als echt extreem lage bpm

'''
