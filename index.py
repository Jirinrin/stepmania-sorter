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

    # temp
    # if previous_title.startswith('<') and '>' in previous_title:
    #     previous_title = previous_title.split('>')[1].strip()

    if previous_title.endswith('>') and '<' in previous_title:
        previous_title = '<'.join(previous_title.split('<')[0:-1]).strip()

    if artist:
        return f'{artist} - {previous_title}'
    return f'{previous_title}{ " <" + ", ".join(new_labels) + ">" if labels else "" }'

def main(check_diff: bool = False):
    
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
            subtitle: str = None
            real_pack_name: str = None
            is_glitchy: bool = False
            has_background_video = False
            diffs = []

            sm_file = os.path.join(song_path, sm_file)
            opened_sm_file = open(sm_file, 'r', -1, 'utf-8')

            diff_counter = -1

            for j, line in enumerate(opened_sm_file):
                if check_diff and diff_counter >= 0:
                    if '#NOTES:' in line:
                        diff_counter = 5
                    if diff_counter == 1:
                        diffs.append( int( line.split(':')[0].strip() ) )
                    if diff_counter > 0:
                        diff_counter -= 1
                    continue
                if not check_diff and j > 100:
                    break
                if j > 50:
                    break
                if not title and '#TITLE:' in line:
                    title = line.split(':')[1].strip().split(';')[0]
                    title_line = j
                elif (not subtitle) and '#SUBTITLE:' in line:
                    subtitle = line.split(':')[1].strip().split(';')[0]
                elif (not artist) and '#ARTIST:' in line:
                    artist = line.split(':')[1].strip().split(';')[0]
                elif not real_pack_name and '#PACK:' in line:
                    real_pack_name = line.split(':')[1].strip().split(';')[0]
                elif not is_glitchy and '#BPMS:' in line and len(line) > GLITCHINESS_CHARS_THRESHOLD:
                    is_glitchy = True
                elif not has_background_video and '#BGCHANGES:' in line and len(line) > 20:
                    has_background_video = True
                elif '#NOTES:' in line:
                    diff_counter = 4

            opened_sm_file.close()

            diffs.sort()

            try:
                print(song_path)
                migration_info = FR.match_song({
                    'artist': artist, 'title': title, 'subtitle': subtitle, 'pack': real_pack_name or pack
                })

                if has_background_video:
                    migration_info['labels'].append('v')
                if is_glitchy:
                    migration_info['labels'].append('g')
                if check_diff:
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
                
            # Uncomment this to just do 1 time until if finds a single match
            # return


# main(True)
main()

print()


'''

pythonding moet ook kunnen: 
collections opsplitsen als grootte over bepaalde threshold 

en nog label voor bijv boven bepaalde bpm, slash als bijv hele nare range, of als echt extreem lage bpm

en missch in het raw ding ook namen met puntkommas delimiten ofzo zodat meer overzicht...?

split artiesten op 'feat' (?)
 
labels toch aan rechterkant van title?

iets van tussenhaakjes in de reference voor termen die weggelaten mogen worden?

een of andere support voor subtitle erbij om bijv. te distinguishen tussen 2 liedjes die zelfde main naam hebben

makkelijke liedjes _echt_ ergens heen verplaatsen want ga toch nooit spelen ofzo

spul van een field kan over meerdere lijnen zijn! => bijv. 'bpms' wat over meerdere regels gaat

verschillende spellingen van 1 artiest / whatever op 1 regel door bijv `//` ertussen

zorg dat de matchende dingen meer prio krijgen dan dingen die via <in> gematched zijn?
slash bijv. <!> of bijv. <prio=2> met default 1 zodat je dat kan configureren 
'''
