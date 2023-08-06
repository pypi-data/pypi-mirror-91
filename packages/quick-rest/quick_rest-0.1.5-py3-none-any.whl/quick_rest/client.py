import requests
from requests.models import Response
import json
from csv import DictWriter
from .exceptions import ServerError, ArgumentError, FormatError
from .resources import strdict


class ServerResponse():
    def __init__(self, response: Response, encoding: str = 'utf-8') -> None:
        self.requests_response = response
        self.raw_content = response.content
        self.encoding = encoding

    def decode(self, encoding: str = '') -> dict:
        if not encoding:
            encoding = self.encoding
        return json.loads((self.raw_content).decode(encoding))

    def to_csv(self, export_path: str, lineterminator: str = '\n', omit_header: bool = False) -> None:
        response = self.decode()
        if len(response) == 1 and isinstance(response, dict):
            data = response[list(response.keys())[0]]
        else:
            raise FormatError('The server response is either not a dict or is a dict with multiple keys.'
                              f' Response is length {len(response)} and type {type(response)}.')
        fields = data[0].keys()
        with open(export_path, 'w', encoding=self.encoding) as csv_file:
            writer = DictWriter(csv_file, fieldnames=fields, lineterminator=lineterminator)
            if not omit_header:
                writer.writeheader()
            for i in data:
                writer.writerow(i)

    def to_txt(self, export_path: str) -> None:
        with open(export_path, 'wb') as txt_file:
            txt_file.write(self.raw_content)


class Client():
    def __init__(self, url: str, encoding: str = 'utf-8', verify: bool = True) -> None:
        self.url = url
        self.encoding = encoding
        self.verify = verify

    def _sanitize_kwargs(self, kwargs):
        headers = {}
        if 'headers' in kwargs.keys():
            headers.update(kwargs.pop('headers'))
        return headers, kwargs

    def _handle_response(self, response: Response) -> ServerResponse:
        code = str(response.status_code)[:1]
        if code not in ('2', '3'):
            raise ServerError(f'{response.status_code}: {response.reason}')
        else:
            return ServerResponse(response, encoding=self.encoding)

    def _call_api_get(self, route: str, **kwargs) -> ServerResponse:
        url = f'{self.url}{route}'
        response = requests.get(url, verify=self.verify, **kwargs)
        return self._handle_response(response)

    def _call_api_post(self, route: str, json_data: dict = {}, text_data: str = '', **kwargs) -> ServerResponse:
        url = f'{self.url}{route}'
        if json_data:
            response = requests.post(url, json=json_data, verify=self.verify, **kwargs)
        elif text_data:
            headers = {}
            if 'headers' in kwargs.keys():
                headers.update(kwargs.pop('headers'))
            headers["Content-Type"] = "text/plain"
            response = requests.post(url, data=text_data, verify=self.verify, **kwargs)
        else:
            raise ArgumentError('Missing arg, need either "json_data" or "text_data".')
        return self._handle_response(response)

    def get(self, route: str, **kwargs) -> ServerResponse:
        return self._call_api_get(route, **kwargs)

    def post(self, route: str, data: strdict = '', **kwargs) -> ServerResponse:
        if isinstance(data, dict):
            return self._call_api_post(route, json_data=data, **kwargs)
        elif isinstance(data, str):
            return self._call_api_post(route, text_data=data, **kwargs)
        else:
            raise ArgumentError('Argument "data" must be of type either either "str" or "dict".')
