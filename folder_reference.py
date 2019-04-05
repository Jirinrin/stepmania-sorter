'Reference for what artists etc. should exist per (sub)folder'

import os
from typing import List
from utility import similar


RAW_REFERENCE_FILE = 'raw_reference.md'
MATCHING_THRESHOLD = 0.5

CRITERION_PRIORITIES = {
    'pack':   0,
    'artist': 1,
    'title':   2
}

def has_higher_priority(current_criterion: str, old_criterion: str) -> int:
    return CRITERION_PRIORITIES[current_criterion] - CRITERION_PRIORITIES[old_criterion]

class FolderReference:
    def __init__(self):
        self.data = {
            'collections': {},
            'labels':  {}
        }

    def match_song(self, song_object):
        best_match = {
            'collection': None,
            'criterion': None,
            'similarity': 0
        }

        for collection, contents in self.data['collections'].items():
            best_matching_criterion = {
                'criterion': None,
                'similarity': 0
            }

            if not contents:
                continue

            for criterion, instances in contents.items():
                highest_similarity = 0

                for instance in instances:
                    rating = similar(instance, song_object[criterion])
                    if rating > MATCHING_THRESHOLD and rating > highest_similarity:
                        highest_similarity = rating

                if highest_similarity > 0 \
                        and ((not best_matching_criterion['criterion']) or has_higher_priority(criterion, best_matching_criterion['criterion']) > 0):
                    best_matching_criterion = {
                        'criterion': criterion,
                        'similarity': highest_similarity
                    }
            
            if best_matching_criterion['criterion'] \
                    and ((not best_match['collection']) \
                        or has_higher_priority(best_matching_criterion['criterion'], best_match['criterion']) > 0 \
                        or (has_higher_priority(best_matching_criterion['criterion'], best_match['criterion']) == 0 \
                            and best_matching_criterion['similarity'] > best_match['similarity'])):
                best_match = {
                    'collection': collection,
                    'criterion': best_matching_criterion['criterion'],
                    'similarity': best_matching_criterion['similarity']
                }

        if not best_match['collection']:
            raise Exception('No match')
                

        object_labels: List[str] = []

        for label, contents in self.data['labels'].items():
            if contents:
                for criterion, instances in contents.items():
                    for instance in instances:
                        if similar(instance, song_object[criterion]) > MATCHING_THRESHOLD:
                            object_labels.append(label)

        return {
            'collection': best_match['collection'],
            'labels': object_labels,
        }




def setup_folder_reference():
    ref = FolderReference()

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
                criterion = line.split('#')[-1].strip()
                ref.data[sub_ref][collection][criterion] = []
            elif line.strip() and criterion:
                ref.data[sub_ref][collection][criterion].append(line.strip())
            
        else:
            if line.startswith('###'):
                sub_ref = 'labels'
            elif line.startswith('##'):
                sub_ref = 'collections'

            if sub_ref:
                collection = line.split('#')[-1].strip()
                ref.data[sub_ref][collection] = {}
        
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
