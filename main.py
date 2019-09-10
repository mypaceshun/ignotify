import os
import datetime
import requests

from ignotify import Client
from requests_oauthlib import OAuth1Session

USERNAME = os.environ.get("IGNOTIFY_USERNAME", "username")
PASSWORD = os.environ.get("IGNOTIFY_PASSWORD", "password")

filename = "var/settings.json"
before_file = "var/before.txt"

USERID = "5823115431"  # rika___n24x
# USERID = "5900738599"  # rikanodorei

CK = os.environ.get("CK")
CS = os.environ.get("CS")
AT = os.environ.get("AT")
AS = os.environ.get("AS")

text = "インスタライブがはじまったよ！！！"
text = "ててて"

access_token = os.environ.get('ACCESS_TOKEN')


def line(message):
    headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/x-www-form-urlencoded',
            }
    data = {
            'message': message,
            }

    res = requests.post('https://notify-api.line.me/api/notify', data=data, headers=headers)
    print(res)

    if res.status_code == '200':
        print('status_code: 200')
    else:
        print('status_code: {}'.format(res.status_code))
        print(res.text)


def main():
    client = Client(USERNAME, PASSWORD,cache_file=filename)
    status = client.broadcast_status(USERID)
    before_status = None

    if os.path.exists(before_file):
        with open(before_file) as file:
            before_status = file.readline()

    with open(before_file, "w") as file:
        file.write(str(status))

    if status is True and before_status == 'False':
        twitter = OAuth1Session(CK, CS, AT, AS)
        params = {"status": text}
        now = datetime.datetime.now()
        print("{}: {}".format(now, text))
        res = twitter.post('https://api.twitter.com/1.1/statuses/update.json', params=params)
        now = datetime.datetime.now()
        print("{}: status code: {}".format(now, res.status_code))
        if res.status_code != 200:
            _error = json.loads(res.text)
            if 'errors' in _error.keys():
                _error = _error['errors'][0]

            for k in _error:
                print("{}: {}: {}".format(now, k, _error[k]))
        line(text)


if __name__ == '__main__':
    main()
