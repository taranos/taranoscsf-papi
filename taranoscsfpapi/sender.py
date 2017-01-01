#
# Taranos Cloud Sonification Framework: Python Pseudo-API
# Copyright 2017 David Hinson, Netrogen Blue LLC (dhinson@netrogenblue.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import json
import urllib.parse
import urllib.request


class Sender (object):
    _last_request_url = None
    _last_request_data = None
    _last_request_data_unquoted = None

    _server_url = 'http://localhost:9000'

    def __init__(self):
        pass

    @staticmethod
    def init(server_url=None):
        global _server_url
        if server_url:
            _server_url = server_url

    @staticmethod
    def report_last_request():
        text = 'url : ' + str(Sender._last_request_url) + '\n'
        text += 'body: ' + str(Sender._last_request_data_unquoted)
        return text

    @staticmethod
    def request(request):
        response_dict = {}
        try:
            response = urllib.request.urlopen(request)

            Sender._last_request_url = request.full_url
            Sender._last_request_data = request.data
            Sender._last_request_data_unquoted = \
                urllib.parse.unquote_plus(request.data.decode('utf-8')) if request.data else None

            response_string = response.read().decode('utf-8')
            response_dict = json.loads(response_string)
        except Exception as exc:
            print(exc)
        return response_dict
        
    def get(self, api_spec):
        url = '%s/%s' % (Sender._server_url, api_spec)

        request = urllib.request.Request(url)
        return self.request(request)

    def put(self, args, form_header, api_spec, method='PUT'):
        if args is None:
            args = []
        elif type(args) is not list:
            args = [args]

        form_list = []
        for arg in args:
            arg_jso = json.dumps(arg() if callable(arg) else arg)
            form_list.append((form_header, arg_jso))

        form_data = None
        if form_list:
            form_data = urllib.parse.urlencode(form_list)
        url = '%s/%s' % (Sender._server_url, api_spec)

        if form_data:
            request = urllib.request.Request(url, data=bytes(form_data, 'utf-8'), method=method)
        else:
            request = urllib.request.Request(url, method=method)
        return self.request(request)

Sender = Sender()
