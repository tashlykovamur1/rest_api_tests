import structlog
from requests import session, JSONDecodeError
import uuid
import curlify

from rest_client.configuration import Configuration


class RestClient:
    def __init__(self, configuration: Configuration):
        self.host = configuration.host
        self.set_headers(configuration.headers)
        self.session = session()
        self.disable_log = configuration.disable_log
        self.log = structlog.get_logger(__name__).bind(service='api')

    def set_headers(self, headers: dict):
        if headers:
            self.session.headers.update(headers)

    def post(self, path: str, **kwargs):
        return self._send_request(method='POST', path=path, **kwargs)

    def get(self, path: str, **kwargs):
        return self._send_request(method='GET', path=path, **kwargs)

    def put(self, path: str, **kwargs):
        return self._send_request(method='PUT', path=path, **kwargs)

    def patch(self, path: str, **kwargs):
        return self._send_request(method='PATCH', path=path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._send_request(method='DELETE', path=path, **kwargs)

    def _send_request(self, method, path, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = f'{self.host}{path}'

        if self.disable_log:
            response = self.session.request(method=method, url=full_url, **kwargs)
            return response

        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data')
        )
        response = self.session.request(method=method, url=full_url, **kwargs)
        curl = curlify.to_curl(response.request)
        print(curl)

        log.msg(
            event='Response',
            status_code=response.status_code,
            headers=response.headers,
            json=self._get_json(response)
        )
        return response

    @staticmethod
    def _get_json(response):
        try:
            return response.json()
        except JSONDecodeError:
            return {}
