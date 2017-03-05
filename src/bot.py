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

    def add_feed(self, chat, args):
        try:
            feed_name = args[1]
        except Exception as e:
            tm.send_message(
                    "/addfeed usage:\n"
                    "\t/addfeed <abbrev of feed>", chat)
            return

        self.add_feed_action(chat, feed_name)


    def add_feed_action(self, chat, feed_name):
        if not Feed.is_valid(feed_name):
            tm.send_message("Invalid feed: {}".format(feed_name), chat)

            return False

        else:
            tm.send_message("Feed added: {}".format(feed_name), chat)
            self.users[chat].add_feed(feed_name)

            if feed_name not in self.feeds.keys():
                self.feeds[feed_name] = Feed(feed_name)

            return True


    def add_filter(self, chat, args):
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
                    "    /addfilter <abbrev of feed> <filter type> <filter argument>", chat)
            return

        if not Filter.is_valid(filter_type):
            tm.send_message("Invalid kind of filter: {}".format(filter_type), chat)
            return

        if not feed_name == None and \
           not self.add_feed_action(chat, feed_name):
            return

        if not self.users[chat].has_last_feed():
            tm.send_message("You need to have at least one feed to add filters", chat)
            return

        self.users[chat].add_filter(Filter(filter_type, filter_args))

        tm.send_message("Filter ({}: {}) added to feed {}".format(
            filter_type, filter_args, self.users[chat].last_feed_added), chat)

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

            if text_words[0] == "/start":
                tm.send_message(\
                    "Hello {},\n"\
                    "Welcome to the arXiv Kitten bot".format(user_name), chat)

            elif text_words[0] == '/addfeed':
                self.add_feed(chat, text_words)

            elif text_words[0] == '/addfilter':
                self.add_filter(chat, text_words)

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
