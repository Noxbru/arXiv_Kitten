from enum import Enum

from entry import Entry

class Filter_Type(Enum):
    AUTHOR  = 1
    TITLE   = 2
    SUMMARY = 3

class Filter:
    filter_type = {
                'author':  Entry.match_author,
                'title':   Entry.match_keyword_in_title,
                'summary': Entry.match_keyword_in_summary
            }
    def __init__(self, type, arg):
        self.fun = self.filter_type[type]
        self.type = type

        self.arg  = arg

    def __str__(self):
        return "{}: {}".format(self.type, self.arg)


    def check_entry(self, entry):
        return self.fun(entry, self.arg)

    @classmethod
    def is_valid(cls, type):
        return type in cls.filter_type.keys()

