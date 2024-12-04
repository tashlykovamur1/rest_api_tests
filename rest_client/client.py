from typing import Any, Dict

import curlify
import structlog
from pydantic import ValidationError
from requests import session, JSONDecodeError, Response, HTTPError
import uuid

from swagger_coverage_py.request_schema_handler import RequestSchemaHandler
from swagger_coverage_py.uri import URI

from rest_client.configuration import Configuration
from rest_client.utils import allure_attach


class ResponseWrapper:
    def __init__(self, status_code: int, headers: Dict[str, Any], cookies: Dict[str, Any], body: Any, error: str = None):
        self.status_code = status_code
        self.headers = headers
        self.cookies = cookies
        self.body = body
        self.error = error


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

    @allure_attach
    def post(self, path: str, **kwargs):
        return self._send_request(method='POST', path=path, **kwargs)

    @allure_attach
    def get(self, path: str, **kwargs):
        return self._send_request(method='GET', path=path, **kwargs)

    @allure_attach
    def put(self, path: str, **kwargs):
        return self._send_request(method='PUT', path=path, **kwargs)

    @allure_attach
    def patch(self, path: str, **kwargs):
        return self._send_request(method='PATCH', path=path, **kwargs)

    @allure_attach
    def delete(self, path: str, **kwargs):
        return self._send_request(method='DELETE', path=path, **kwargs)

    def _send_request(self, method, path, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = f'{self.host}{path}'

        if self.disable_log:
            response = self.session.request(method=method, url=full_url, **kwargs)
            response.raise_for_status()
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

        # coverage
        url = URI(host=self.host, base_path="", unformatted_path=path, uri_params=kwargs.get("params"))
        RequestSchemaHandler(
            uri=url, method=method.lower(), response=response, kwargs=kwargs
        ).write_schema()

        log.msg(
            event='Response',
            status_code=response.status_code,
            headers=response.headers,
            json=self._get_json(response)
        )
        response.raise_for_status()
        return response

    @staticmethod
    def _get_json(response):
        try:
            return response.json()
        except JSONDecodeError:
            return {}

    @staticmethod
    def format_response(
            response: Response,
            response_schema: Any,
            empty_body: bool = False,
    ) -> ResponseWrapper:
        """Format and return response"""
        error = None
        try:
            body = (
                response.text
                if empty_body
                else response_schema(
                    many=True if isinstance(response.json(), list) else None
                ).load(response.json())
            )
        except (ValidationError, JSONDecodeError, TypeError, HTTPError) as exc:
            body = (
                response.json()
                if response.text.startswith("{") and response.text.endswith("}")
                else response.text
            )
            error = f"Incorrect response: {exc}"

        return ResponseWrapper(
            status_code=response.status_code,
            headers=dict(response.headers),
            cookies=dict(response.cookies),
            body=body,
            error=error
        )
