from dbhelper import DBHelper
from user import User
from feed import Feed

import telegram as tm

import pprint as pp
import time

class arXiv_Kitten_bot:
    def __init__(self):
        self.users = {}

    def handle_updates(self, updates):
        for update in updates['result']:
            text      = update['message']['text']
            chat      = update['message']['chat']['id']
            user_name = update['message']['chat']['username']

            if chat not in self.users.keys():
                self.users[chat] = User(chat, user_name)
                print("Created new user: {}".format(user_name))

            if text == "/start":
                tm.send_message(\
                    "Hello {},\n"\
                    "Welcome to the arXiv Kitten bot".format(user_name), chat)

            elif text.startswith('/addfeed'):
                try:
                    feed_name = text.split(' ')[1]
                except Exception as e:
                    tm.send_message(
                            "/addfeed usage:\n"
                            "\t/addfeed <abbrev of feed>", chat)
                    continue

                if not Feed.is_valid(feed_name):
                    tm.send_message("Invalid feed: {}".format(feed_name), chat)
                else:
                    tm.send_message("Feed added: {}".format(feed_name), chat)
                    self.users[chat].add_feed(feed_name)

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
