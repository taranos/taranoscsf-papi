#
# Taranos Cloud Sonification Framework: Python Pseudo-API
# Copyright (C) 2018 David Hinson, Netrogen Blue LLC (dhinson@netrogenblue.com)
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


class SingleSender:


    default_server_url = 'http://localhost:9000'

    class __InnerSender:

        def __init__(self, server_url=None, is_verbose=False):
            self._is_verbose = is_verbose
            self._last_request_data = None
            self._last_request_data_unquoted = None
            self._last_request_url = None
            self._last_response_string = None
            self._request_count = 0
            self._server_url = server_url if server_url else SingleSender.default_server_url

        def report_last_request(self):
            text = '\n' + 'Request #' + str(self._request_count) + '\n'
            text += '|request url : ' + str(self._last_request_url) + '\n'
            text += '|request body: ' + str(self._last_request_data_unquoted) + '\n'
            text += '|response    : ' + str(self._last_response_string)
            return text

        def request(self, request):
            response_dict = {}
            try:
                self._request_count += 1

                response = urllib.request.urlopen(request)

                self._last_request_url = request.full_url
                self._last_request_data = request.data
                self._last_request_data_unquoted = \
                    urllib.parse.unquote_plus(request.data.decode('utf-8')) if request.data else None

                response_string = response.read().decode('utf-8')
                self._last_response_string = response_string
                response_dict = json.loads(response_string)

                if self._is_verbose:
                    print(self.report_last_request())

            except Exception as exc:
                print(exc)
            return response_dict
        
        def get(self, api_spec):
            url = '%s/%s' % (self._server_url, api_spec)

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
            url = '%s/%s' % (self._server_url, api_spec)

            if form_data:
                request = urllib.request.Request(url, data=bytes(form_data, 'utf-8'), method=method)
            else:
                request = urllib.request.Request(url, method=method)
            return self.request(request)

    _instance = None

    def __init__(self, server_url=None, is_verbose=False):
        if not SingleSender._instance:
            SingleSender._instance = SingleSender.__InnerSender(server_url, is_verbose)
        else:
            SingleSender._instance._server_url = server_url
            SingleSender._instance._is_verbose = is_verbose

    def __getattr__(self, name):
        return getattr(self._instance, name)

Sender = SingleSender()
