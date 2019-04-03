'Utility functions for other modules to use'

from difflib import SequenceMatcher

def similar(string_1: str, string_2: str):
    return SequenceMatcher(None, string_1.lower(), string_2.lower()).ratio()
