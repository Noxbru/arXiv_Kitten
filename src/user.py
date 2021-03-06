import telegram as tm
from filter import Filter

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.feeds = {}
        self.editing_feed = None

    def add_feed(self, feed_name):
        if self.has_feed(feed_name):
            tm.send_message("Feed already exists: {}".format(feed_name), self.id)
        else:
            tm.send_message("Feed added: {}".format(feed_name), self.id)
            self.feeds[feed_name] = []

        self.editing_feed = feed_name

    def add_filter(self, filter_type, filter_args):
        if not self.has_editing_feed():
            tm.send_message("You need to have at least one feed to add filters", self.id)
            return

        self.feeds[self.editing_feed] += [Filter(filter_type, filter_args)]

        tm.send_message("Filter ({}: {}) added to feed {}".format(
            filter_type, filter_args, self.editing_feed), self.id)

    def delete_feed(self, feed_name):
        if self.has_feed(feed_name):
            tm.send_message("Feed deleted: {}".format(feed_name), self.id)
            self.feeds.pop(feed_name)
        else:
            tm.send_message("You don't have the feed: {}".format(feed_name), self.id)


    def delete_filter(self, filter_type, filter_args):
        feed_filters = self.feeds[self.editing_feed]
        for (i, f) in enumerate(feed_filters):
            if f.type == filter_type and f.arg == filter_args:
                del feed_filters[i]

                tm.send_message("Deleted filter ({}: {}) from feed {}".format(
                    filter_type, filter_args, self.editing_feed), self.id)

                return
        else:
            tm.send_message("Filter ({}: {}) not found in feed {}".format(
                filter_type, filter_args, self.editing_feed), self.id)


    def edit_feed(self, feed_name):
        if not self.has_feed(feed_name):
            tm.send_message("Feed doesn't exist: {}".format(feed_name), self.id)
            return

        self.editing_feed = feed_name
        tm.send_message("Editing Feed: {}".format(feed_name), self.id)


    def has_feed(self, feed_name):
        return feed_name in self.feeds.keys()

    def has_editing_feed(self):
        return self.editing_feed != None
