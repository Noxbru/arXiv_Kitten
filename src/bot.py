from dbhelper import DBHelper
from user import User
from feed import Feed
from filter import Filter

import telegram as tm

import pprint as pp
import time
import re

class arXiv_Kitten_bot:
    def __init__(self):
        self.users = {}
        self.feeds = {}

    def add_feed(self, user, args):
        try:
            feed_name = args[1]
        except Exception as e:
            tm.send_message(
                    "/addfeed usage:\n"
                    "\t/addfeed <abbrev of feed>", user.id)
            return

        if not Feed.is_valid(feed_name):
            tm.send_message("Invalid feed: {}".format(feed_name), user.id)

        if user.has_feed(feed_name):
            tm.send_message("Feed already exits: {}".format(feed_name), user.id)
            user.last_feed_added = feed_name

        else:
            tm.send_message("Feed added: {}".format(feed_name), user.id)
            user.add_feed(feed_name)

            if feed_name not in self.feeds.keys():
                self.feeds[feed_name] = Feed(feed_name)


    def add_filter(self, user, args):
        feed_name = None

        if len(args) == 3:
            filter_type = args[1]
            filter_args = args[2]
        elif len(args) == 4:
            feed_name   = args[1]
            filter_type = args[2]
            filter_args = args[3]

        else:
            tm.send_message(
                    "/addfilter usage:\n" \
                    "    /addfilter <filter type> <filter argument>\n" \
                    "    /addfilter <abbrev of feed> <filter type> <filter argument>", user.id)
            return

        if not Filter.is_valid(filter_type):
            tm.send_message("Invalid kind of filter: {}".format(filter_type), user.id)
            return

        # embeded add_feed function without some of the messages
        # and without validation of the extraction of feed_name
        if feed_name != None:
            if not Feed.is_valid(feed_name):
                tm.send_message("Invalid feed: {}".format(feed_name), user.id)
                return
            if user.has_feed(feed_name):
                user.last_feed_added = feed_name
            else:
                tm.send_message("Feed added: {}".format(feed_name), user.id)
                user.add_feed(feed_name)

                if feed_name not in self.feeds.keys():
                    self.feeds[feed_name] = Feed(feed_name)

        if not user.has_last_feed():
            tm.send_message("You need to have at least one feed to add filters", user.id)
            return

        user.add_filter(Filter(filter_type, filter_args))

        tm.send_message("Filter ({}: {}) added to feed {}".format(
            filter_type, filter_args, user.last_feed_added), user.id)


    def list_filters(self, user, args):
        for (feed_abbrv, filters) in user.feeds.items():
            tm.send_message("Filters for feed: {}".format(feed_abbrv), user.id)

            for filter in filters:
                tm.send_message("\t+ {}".format(filter), user.id)


    def handle_updates(self, updates):
        for update in updates['result']:
            if 'message' not in update.keys(): continue

            text      = update['message']['text']
            chat      = update['message']['chat']['id']
            user_name = update['message']['chat']['username']

            text_words = re.findall(r'\"[^\"]*\"|\S+', text)

            if chat not in self.users.keys():
                self.users[chat] = User(chat, user_name)
                print("Created new user: {}".format(user_name))

            user = self.users[chat]

            if text_words[0] == "/start":
                tm.send_message(\
                    "Hello {},\n"\
                    "Welcome to the arXiv Kitten bot".format(user_name), user.id)

            elif text_words[0] == '/addfeed':
                self.add_feed(user, text_words)

            elif text_words[0] == '/addfilter':
                self.add_filter(user, text_words)

            elif text_words[0] == '/listfilters':
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
