from enum import Enum

from entry import Entry

class Filter_Type(Enum):
    AUTHOR  = 1
    TITLE   = 2
    SUMMARY = 3

class Filter:
    def __init__(self, type, arg):
        self.fun = {
                Filter_Type.AUTHOR:  Entry.match_author,
                Filter_Type.TITLE:   Entry.match_keyword_in_title,
                Filter_Type.SUMMARY: Entry.match_keyword_in_summary
            }[type]

        self.arg  = arg

    def check_entry(self, entry):
        return self.fun(entry, self.arg)

