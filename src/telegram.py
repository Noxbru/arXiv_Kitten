import json
import requests
import urllib

from config import BOT_URL

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


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)
