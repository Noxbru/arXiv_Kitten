class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.feeds = {}
        self.last_feed_added = None

    def add_feed(self, feed_name):
        self.feeds[feed_name] = []
        self.last_feed_added = feed_name

    def add_filter(self, filter):
        self.feeds[self.last_feed_added] += [filter]

    def has_last_feed(self):
        return self.last_feed_added != None
