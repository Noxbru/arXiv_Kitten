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
        if self.last_feed_added == None:
            return None

        self.feeds[self.last_feed_added] += [filter]
