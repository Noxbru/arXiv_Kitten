from config import BOT_URL
from dbhelper import DBHelper

import json
import requests
import time
import urllib

import pprint as pp

PP = pp.PrettyPrinter()

db = DBHelper()


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)

    return json.loads(content)


def get_updates(offset = None):
    update_base_url = BOT_URL + "getUpdates?timeout=90"

    if offset == None:
        url = update_base_url
    else:
        url = update_base_url + "&offset={}".format(offset)

    return get_json_from_url(url)

def get_last_update_id(updates):
    update_ids = []

    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))

    return max(update_ids)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup = None):
    text = urllib.parse.quote_plus(text)

    url = BOT_URL + "sendMessage?text={}&chat_id={}" \
                    "&parse_mode=Markdown".format(text, chat_id)

    if reply_markup != None:
        url += "&reply_markup={}".format(reply_markup)

    get_url(url)

def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items(chat)

        if text == "/start":
            send_message("Welcome to the TO DO bot", chat)

        elif text == "/done":
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)

        elif text.startswith('/'):
            continue

        elif text in items:
            db.delete_item(text, chat)
            items = db.get_items(chat)
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)

        else:
            db.add_item(text, chat)
            items = db.get_items(chat)
            message = "\n".join(items)
            send_message(message, chat)

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            pp.pprint(updates)
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
