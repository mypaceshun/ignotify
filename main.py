import os
import json
import codecs
from instagram_private_api import Client

USERNAME = os.environ.get("IGNOTIFY_USERNAME", "username")
PASSWORD = os.environ.get("IGNOTIFY_PASSWORD", "password")

filename = "var/settings.json"

# USERID = "5823115431"  # rika___n24x
USERID = "5900738599"  # rikanodorei


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object

def main():
    print("main")
    if os.path.exists(filename):
        with open(filename) as infile:
            caches_settings = json.load(infile, object_hook=from_json)
            api = Client(USERNAME, PASSWORD, settings=caches_settings)
    else:
        api = Client(USERNAME, PASSWORD)
        cache_settings = api.settings
        with open(filename, 'w') as outfile:
            json.dump(cache_settings, outfile, default=to_json)
            print('SAVED: {0!s}'.format(filename))
    results = api.user_info(USERID)
    print(results)
    print(api.authenticated_user_id)

    res = api.user_story_feed(USERID)
    print(res)

if __name__ == '__main__':
    main()
