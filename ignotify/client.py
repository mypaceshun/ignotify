import codecs
import json
import os
from logging import getLogger

from instagram_private_api import Client as igclient
from instagram_private_api import (ClientCookieExpiredError, ClientError,
                                   ClientLoginError, ClientLoginRequiredError)

logger = getLogger(__name__)


class IGNotifyError(Exception):
    pass


class Client():
    def __init__(self,
                 username,
                 password,
                 cache_file="settings.json"):
        self.username = username
        self.password = password
        self.cache_file = cache_file
        self.login()

    def to_json(self, python_object):
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': codecs.encode(python_object, 'base64').decode()}
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    def from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object

    def login(self):
        # https://github.com/ping/instagram_private_api/blob/master/examples/savesettings_logincallback.py
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file) as infile:
                    caches_settings = json.load(
                        infile, object_hook=self.from_json)
                    self.api = igclient(self.username, self.password,
                                        settings=caches_settings)
            else:
                self.api = igclient(self.username, self.password)
                cache_settings = self.api.settings
                with open(self.cache_file, 'w') as outfile:
                    json.dump(cache_settings, outfile, default=self.to_json)
                    logger.info('SAVED: {0!s}'.format(self.cache_file))
        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            logger.warn(
                'ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

            # Login expired
            # Do relogin but use default ua, keys and such
            self.api = igclient(self.username, self.password)
            cache_settings = self.api.settings
            with open(self.cache_file, 'w') as outfile:
                json.dump(cache_settings, outfile, default=self.to_json)
                logger.info('SAVED: {0!s}'.format(self.cache_file))

        except ClientLoginError as e:
            msg = 'ClientLoginError {0!s}'.format(e)
            logger.error(msg)
            IGNotifyError(msg)
        except ClientError as e:
            msg = 'ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(
                e.msg, e.code, e.error_response)
            logger.error(msg)
            IGNotifyError(msg)
        except Exception as e:
            msg = 'Unexpected Exception: {0!s}'.format(e)
            logger.error(msg)
            IGNotifyError(msg)

    def search(self, keyword):
        res = self.api.search_users(keyword)
        users = res['users']
        return users

    def broadcast_status(self, userid):
        res = self.api.user_story_feed(userid)
        if res['broadcast'] is not None:
            if res['broadcast']['broadcast_status'] == 'active':
                return True
        return False
