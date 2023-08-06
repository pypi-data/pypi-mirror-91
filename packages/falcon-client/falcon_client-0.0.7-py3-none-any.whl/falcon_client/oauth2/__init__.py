import requests
# import requests_cache
import tempfile
from pathlib import Path
import pickle
import time
from base64 import b64encode


TEMP_FOLDER = Path(tempfile.gettempdir())
NOW = int(time.time())
# requests_cache.install_cache(Path.joinpath(TEMP_FOLDER, 'requests').as_posix())
cached_creds = Path.joinpath(TEMP_FOLDER, 'falcon.cache')


class AuthMixin:
    def login(self, api_endpoint='/oauth2/token'):
        # Read cached token and check validity.
        if self.cache_creds:
            try:
                if cached_creds.exists():
                    try:
                        _headers = pickle.load(cached_creds.open('rb'))
                    except:
                        pass
                    else:
                        # Check cached token validity
                        if NOW < int(cached_creds.stat().st_ctime) + int(_headers['expires_in']):
                            self.req.headers = _headers
                            return
            except:
                self.logger.debug("Credential cache file not found.")

        # Cached token not found or invalid.  Request new token.
        r_data = {'client_id': self.client_id, 'client_secret': self.client_key}
        try:
            _resp = self.req.post(self.BASE_URL + api_endpoint, data=r_data)
        except:
            raise
        else:
            try:
                if _resp.ok:
                    self.req.headers['Authorization'] = "Bearer {}".format(_resp.json()['access_token'])
                    self.req.headers['expires_in'] = str(_resp.json().get('expires_in', '1798'))
                    # Cache credentials
                    try:
                        if self.cache_creds:
                            pickle.dump(self.req.headers, cached_creds.open('wb'))
                    except:
                        pass
                else:
                    raise requests.HTTPError(_resp.json()['errors'])
            except:
                try:
                    errors = _resp.json()['errors']
                except:
                    errors = _resp.content
                raise requests.HTTPError(errors)

    def logout(self, oauth_endpoint='/oauth2/revoke'):
        r_data = {'token': self.req.headers['Authorization'].replace('Bearer ', '', 1)}
        basic_auth = b64encode("{}:{}".format(self.client_id, self.client_key).encode()).strip()
        self.req.headers['Authorization'] = "Basic {}".format(basic_auth.decode())
        try:
            _resp = self.req.post(self.BASE_URL + oauth_endpoint, data=r_data)
            try:
                if self.cache_creds:
                    cached_creds.unlink()
            except Exception as err:
                self.logger.warning("Failed to remove cached credential file (%s). %s" % (cached_creds.as_posix(), err))
        except:
            raise
        else:
            try:
                errors = _resp.json()['errors']
            except:
                errors = _resp.content
            self.logger.error(errors)
