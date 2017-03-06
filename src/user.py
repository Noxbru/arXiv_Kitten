class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.feeds = {}
        self.editing_feed = None

    def add_feed(self, feed_name):
        self.feeds[feed_name] = []
        self.editing_feed = feed_name

    def add_filter(self, filter):
        self.feeds[self.editing_feed] += [filter]

    def has_feed(self, feed_name):
        return feed_name in self.feeds.keys()

    def has_editing_feed(self):
        return self.editing_feed != None
