import json

import allure
import curlify
import requests


def allure_attach(fn):
    def wrapper(*args, **kwargs):
        body = kwargs.get('json')
        if body:
            allure.attach(
                json.dumps(kwargs.get('json'), indent=2),
                name='request',
                attachment_type=allure.attachment_type.JSON
            )
        response = fn(*args, **kwargs)
        curl = curlify.to_curl(response.request)
        allure.attach(curl, name="curl", attachment_type=allure.attachment_type.TEXT)

        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            response_text = response.text
            status_code = f'< status_code {response.status_code} >'
            allure.attach(
                response_text if len(response_text) > 0 else status_code,
                name='response',
                attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                json.dumps(response_json, indent=2),
                name='response',
                attachment_type=allure.attachment_type.JSON
            )
        return response

    return wrapper
