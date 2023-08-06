from requests.models import Response
import requests
import json


# api response structure
class APIResponse:
    """
    A simple class to process RESTful JSON API responses
    if the response is not in JSON format, it is assumed to be unsuccessful
    """
    def __repr__(self):
        return "cs_falcon_api::Response"

    def __init__(self, response_object, err_message=None):
        assert isinstance(response_object, Response)
        self.status_code = response_object.status_code
        if response_object.ok:
            self.success = True
        else:
            self.success = False

        try:
            _resp = response_object.json()
            self.data = _resp['resources'] if 'resources' in _resp.keys() else []
            self.errors = _resp['errors'] if 'errors' in _resp.keys() else []
            self.meta = _resp['meta'] if 'meta' in _resp.keys() else []
        except:
            self.data = []
            self.errors = [{"code": self.status_code,
                            "message": err_message or response_object.content.decode('utf-8', errors="ignore")
                            }]
            self.meta = []


class APIClientMixin:
    def api_call(self, endpoint, payload={}, params={}, timeout=150):
        self.req.headers['Content-Type'] = "application/x-www-form-urlencoded"
        self.req.headers['Accept'] = "application/json"
        try:
            _resp = APIResponse(self.req.post(self.BASE_URL + endpoint, data=json.dumps(payload),
                                              params=params, timeout=timeout))
            if _resp.status_code == 401:
                self.login()
                _resp = APIResponse(self.req.post(self.BASE_URL + endpoint, data=json.dumps(payload),
                                                  params=params, timeout=timeout))

        except:
            raise
        else:
            return _resp

    def api_query(self, endpoint, params={}, timeout=150):
        self.req.headers['Accept'] = "application/json"
        try:
            _resp = APIResponse(self.req.get(self.BASE_URL + endpoint, params=params, timeout=timeout))
            if _resp.status_code == 401:
                self.login()
                _resp = APIResponse(self.req.get(self.BASE_URL + endpoint, params=params, timeout=timeout))
        except Exception as err:
            self.logger.error('API query failure.')
            try:
                errors = _resp.errors
            except:
                errors = err
            raise requests.HTTPError(errors)
        else:
            if _resp.success:
                return _resp
            else:
                raise requests.HTTPError(_resp.errors)
