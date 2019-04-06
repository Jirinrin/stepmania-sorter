'Script for arranging OpenITG collection'

import os
from typing import List

from utility import safe_move, format_for_windows
from folder_reference import FOLDER_REFERENCE as FR

print()

SONGS_DIR = r'F:\voorSnelkoppelingen\H\OpenITG\Songs'
# NEW_SONGS_DIR = r'F:\voorSnelkoppelingen\H\OpenITG\SongsOrganised'

GLITCHINESS_CHARS_THRESHOLD = 150
EASY_THRESHOLD = 6
HARD_THRESHOLD = 14

def format_title(raw_previous_title: str, labels: List[str], artist: str = None):
    # als previous title al labels heeft snij dat deel dan eerst weg
    new_labels = map(lambda l: l.split(':')[-1].strip(), labels)
    previous_title = raw_previous_title.strip()
    if raw_previous_title.startswith('<') and '>' in raw_previous_title:
        previous_title = raw_previous_title.split('>')[1].strip()

    return f'{ artist + " - " if artist else ("<" + ", ".join(new_labels) + "> " if labels else "") }{previous_title}'
    


def main(check_diff: bool):
    
    if not os.path.exists(SONGS_DIR):
        raise Exception('Path doesn\'t exist')
    
    pack_folders: List[str] = os.listdir(SONGS_DIR)

    for i, pack in enumerate(pack_folders):
        # if i > 6:
        #     break

        col_path = os.path.join(SONGS_DIR, pack)
        song_folders = os.listdir(col_path)


        for song in song_folders:
            song_path = os.path.join(col_path, song)

            if os.path.isfile(song_path):
                continue

            files = os.listdir(song_path)
            # TODO: test if you can just get filter()[0]
            sm_file  = next(filter(lambda x: x.split('.')[-1] == 'sm', files), None)

            if not sm_file:
                continue

            artist: str = None
            title: str = None
            title_line: int = None
            real_pack_name: str = None
            is_glitchy: bool = False
            has_background_video = False
            diffs = []

            sm_file = os.path.join(song_path, sm_file)
            opened_sm_file = open(sm_file, 'r', -1, 'utf-8')

            diff_counter = -1

            print(song_path)
            for j, line in enumerate(opened_sm_file):
                print(j)
                if check_diff and diff_counter >= 0:
                    if line.startswith('#NOTES:'):
                        diff_counter = 5
                    if diff_counter == 1:
                        diffs.append( int( line.split(':')[0].strip() ) )
                    if diff_counter > 0:
                        diff_counter -= 1
                    continue
                if not title and line.startswith('#TITLE:'):
                    title = line.split(':')[-1].strip().split(';')[0]
                    title_line = j
                elif not artist and line.startswith('#ARTIST:'):
                    artist = line.split(':')[-1].strip().split(';')[0]
                elif not real_pack_name and line.startswith('#PACK:'):
                    real_pack_name = line.split(':')[-1].strip().split(';')[0]
                elif not is_glitchy and line.startswith('#BPMS:') and len(line) > GLITCHINESS_CHARS_THRESHOLD:
                    is_glitchy = True
                elif not has_background_video and line.startswith('#BGCHANGES:') and len(line) > 20:
                    has_background_video = True
                elif line.startswith('#NOTES:'):
                    diff_counter = 4

            opened_sm_file.close()

            diffs.sort()
            print(diffs)

            try:
                migration_info = FR.match_song({
                    'artist': artist, 'title': title, 'pack': real_pack_name or pack
                })

                if has_background_video:
                    migration_info['labels'].append('v')
                if is_glitchy:
                    migration_info['labels'].append('g')
                if diffs[-1] < EASY_THRESHOLD:
                    migration_info['labels'].append('e')
                if diffs[0] > HARD_THRESHOLD:
                    migration_info['labels'].append('h')

                new_title = format_title(title, migration_info['labels'])
                new_folder_name = format_for_windows(format_title(title, migration_info['labels'], artist))

                print(migration_info, artist, '-', title, '(', pack, ')')
                print(new_folder_name)

                # also write it in the file

                # TODO: Could do this with temporary copy or sth
                opened_sm_file = open(sm_file, 'r', -1, 'utf-8')
                lines = opened_sm_file.read().splitlines()
                lines[title_line] = f'#TITLE:{new_title};'
                if not real_pack_name:
                    lines.insert(0, f'#PACK:{pack};')
                    lines.insert(1, f'#ORIGINAL_NAME:{song};')
                opened_sm_file.close()
                writing_sm_file = open(sm_file,'w', -1, 'utf-8')
                writing_sm_file.write('\n'.join(lines))
                writing_sm_file.close()

                safe_move(
                    os.path.join(SONGS_DIR, pack, song),
                    os.path.join(SONGS_DIR, '__' + migration_info['collection'] + '__'),
                    new_folder_name
                )
                
            except Exception as e:
                if str(e) == 'No match':
                    continue
                else:
                    raise e

                
            return


main(True)

print()


'''

Functionality:
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

en missch in het raw ding ook namen met puntkommas delimiten ofzo zodat meer overzicht...?

split artiesten op 'feat' (?)
 
labels toch aan rechterkant van title?
'''
