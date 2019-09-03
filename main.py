import os
from pprint import pprint

from ignotify import Client

USERNAME = os.environ.get("IGNOTIFY_USERNAME", "username")
PASSWORD = os.environ.get("IGNOTIFY_PASSWORD", "password")

filename = "var/settings.json"

# USERID = "5823115431"  # rika___n24x
USERID = "5900738599"  # rikanodorei


def main():
    print("main")
    client = Client(USERNAME, PASSWORD,cache_file=filename)
    users = client.search('rikanodorei')
    for user in users:
        params = {'id': user['pk'],
                  'username': user['username'],
                  'full_name': user['full_name']}
        txt = "id: {id}, username: {username}, full_name: {full_name}"
        print(txt.format(**params))
    s = client.broadcast_status(USERID)
    print(s)
    # results = api.user_info(USERID)
    # pprint(results)
    # res = api.user_story_feed(USERID)
    # pprint(res)
    # id = "17853844132534704"
    # res = api.broadcast_info(id)
    # pprint(res)
    # res = api.broadcast_comment(id, 'test')
    # pprint(res)


if __name__ == '__main__':
    main()
