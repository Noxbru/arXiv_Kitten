from config import BOT_URL

import json
import requests
import time
import urllib

import pprint as pp

PP = pp.PrettyPrinter()


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


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = BOT_URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            pp.pprint(updates)
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
