class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.feeds = set()

    def add_feed(self, feed_name):
        self.feeds.add(feed_name)
