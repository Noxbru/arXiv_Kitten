from dbhelper import DBHelper
from user import User
from feed import Feed
from filter import Filter

import telegram as tm

import pprint as pp
import time
import shlex

class arXiv_Kitten_bot:
    def __init__(self):
        self.users = {}
        self.feeds = {}

    def add_feed(self, user, args):
        try:
            feed_name = args[1]
        except Exception as e:
            tm.send_message(
                    "/add\_feed usage:\n"
                    "\t/add\_feed <abbrev of feed>", user.id)
            return

        if not Feed.is_valid(feed_name):
            tm.send_message("Invalid feed: {}".format(feed_name), user.id)
            return

        user.add_feed(feed_name)

        if not self.has_feed(feed_name):
            self.feeds[feed_name] = Feed(feed_name)


    def add_filter(self, user, args):
        if len(args) == 3:
            filter_type = args[1]
            filter_args = args[2]
        else:
            tm.send_message(
                    "/add\_filter usage:\n" \
                    "\t/add\_filter <filter type> <filter argument>", user.id)
            return

        if not Filter.is_valid(filter_type):
            tm.send_message("Invalid kind of filter: {}".format(filter_type), user.id)
            return

        user.add_filter(filter_type, filter_args)


    def add_filter_to_feed(self, user, args):
        if len(args) == 4:
            feed_name   = args[1]
            filter_type = args[2]
            filter_args = args[3]
        else:
            tm.send_message(
                    "/add\_filter\_to\_feed usage:\n" \
                    "\t/add\_filter\_to\_feed <abbrev of feed> <filter type> <filter argument>", user.id)
            return

        if not Feed.is_valid(feed_name):
            tm.send_message("Invalid feed: {}".format(feed_name), user.id)
            return

        if not Filter.is_valid(filter_type):
            tm.send_message("Invalid kind of filter: {}".format(filter_type), user.id)
            return

        # embeded add_feed function without some of the messages
        # and without validation of the extraction of feed_name
        if user.has_feed(feed_name):
            user.editing_feed = feed_name
        else:
            user.add_feed(feed_name)

            if not self.has_feed(feed_name):
                self.feeds[feed_name] = Feed(feed_name)

        user.add_filter(filter_type, filter_args)


    def delete_feed(self, user, args):
        if len(args) == 2:
            feed_name = args[1]
        else:
            tm.send_message(
                    "/delete\_feed usage:\n" \
                    "\t/delete\_feed <feed name>", user.id)
            return

        user.delete_feed(feed_name)

        for us in self.users.values():
            if us.has_feed(feed_name):
                return
        else:
            self.feeds.pop(feed_name)

    def delete_filter(self, user, args):
        if len(args) == 3:
            filter_type = args[1]
            filter_args = args[2]
        else:
            tm.send_message(
                    "/delete\_filter usage:\n" \
                    "\t/delete\_filter <filter type> <filter argument>", user.id)
            return

        if not Filter.is_valid(filter_type):
            tm.send_message("Invalid kind of filter: {}".format(filter_type), user.id)
            return

        user.delete_filter(filter_type, filter_args)


    def edit_feed(self, user, args):
        if len(args) == 2:
            feed_name = args[1]
        else:
            tm.send_message(
                    "/edit\_feed usage:\n" \
                    "\t/edit\_feed <feed name>", user.id)
            return

        user.edit_feed(feed_name)


    def list_feeds(self, user, args):
        msg = "Feeds for user: {}\n".format(user.name)
        for feed_name in user.feeds.keys():
            msg += "\t+ {}\n".format(feed_name)

        tm.send_message(msg, user.id)


    def list_filters(self, user, args):
        msg = ""
        for (feed_abbrv, filters) in user.feeds.items():
            msg += "Filters for feed: {}\n".format(feed_abbrv)

            for filter in filters:
                msg += "\t+ {}\n".format(filter)

        tm.send_message(msg, user.id)


    def send_entry(self, entry, user):
        tm.send_message(entry.format_entry(), user.id)


    def has_feed(self, feed_name):
        return feed_name in self.feeds.keys()

    def handle_updates(self, updates):
        for update in updates['result']:
            if 'message' not in update.keys(): continue

            text      = update['message']['text']
            chat      = update['message']['chat']['id']
            user_name = update['message']['chat']['username']

            text_words = shlex.split(text)

            if chat not in self.users.keys():
                self.users[chat] = User(chat, user_name)
                print("Created new user: {}".format(user_name))

            user = self.users[chat]

            if text_words[0] == "/start":
                tm.send_message(\
                    "Hello {},\n"\
                    "Welcome to the arXiv Kitten bot".format(user_name), user.id)

            elif text_words[0] == '/add_feed':
                self.add_feed(user, text_words)

            elif text_words[0] == '/add_filter':
                self.add_filter(user, text_words)

            elif text_words[0] == '/add_filter_to_feed':
                self.add_filter_to_feed(user, text_words)

            elif text_words[0] == '/delete_feed':
                self.delete_feed(user, text_words)

            elif text_words[0] == '/delete_filter':
                self.delete_filter(user, text_words)

            elif text_words[0] == '/edit_feed':
                self.edit_feed(user, text_words)

            elif text_words[0] == '/list_feeds':
                self.list_feeds(user, text_words)

            elif text_words[0] == '/list_filters':
                self.list_filters(user, text_words)

            elif text.startswith('/'):
                continue


PP = pp.PrettyPrinter()
kitten = arXiv_Kitten_bot()

def main():
    last_update_id = None

    while True:
        updates = tm.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            pp.pprint(updates)
            last_update_id = tm.get_last_update_id(updates) + 1
            kitten.handle_updates(updates)

        time.sleep(0.5)

if __name__ == '__main__':
    main()
