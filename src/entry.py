import re

class Entry:
    def __init__(self, entry):
        self.id      = entry['id']
        self.authors = Entry.get_authors(entry['author'])
        self.summary = Entry.get_summary(entry['summary'])
        self.title   = Entry.get_title(entry['title'])

    def __str__(self):
        return "Id of entry: {}\n" \
                "Title of entry: {}\n" \
                "Authors of entry: {}\n" \
                "Summary of entry: {}" \
                .format(self.id, self.title, self.authors, self.summary)

    def match_author(self, _author):
        for author in self.authors:
            if author.lower() == _author.lower():
                return True
        else:
            return False

    def match_keyword_in_title(self, keyword):
        regex = re.compile(r'\b{}\b'.format(keyword), re.I)
        return regex.search(self.title)

    def match_keyword_in_summary(self, keyword):
        regex = re.compile(r'\b{}\b'.format(keyword), re.I)
        return regex.search(self.summary)


    def get_authors(authors):
        regex = re.compile(u" *\<a href=.*\>(?P<author>.*)\<\/a\>")

        authors = authors.split(',')

        _authors = []
        for author in authors:
            try:
                _author = regex.match(author).group('author')
                _authors.append(_author)
            except Exception as e:
                print("Author giving problems: ")
                print(" -> {}".format(author))
                pass

        return _authors

    def get_summary(summary):
        summary = summary.replace('\n', ' ')

        if summary[:3] == "<p>" and \
        summary[-4:] == "</p>":
            summary = summary[3:-4]

        return summary

    def get_title(title):
        return title
