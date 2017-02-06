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

from taranoscsfpapi.api import *


#
# Cell:
#

# Destroy:

class CellDestructor:
    def __init__(self,
                 is_testing):
        self.is_testing = is_testing

    def __call__(self):
        request_dict = {}
        if self.is_testing:
            request_dict['t'] = '1'
        return request_dict


def destroy_cell(*, is_testing=False):
    """
    Destroy (reset) the currently associated simulation cell.

    :return: Cell destruction report
    """
    response_dict = Sender.put(CellDestructor(is_testing), 'dc', 'tmp/c', method='DELETE')

    get_server_defaults()

    return handle_response(response_dict, None)


# Report:

def report_cell(*, sections=None):
    """
    Report the currently associated cell's configuration.

    :param sections: Reporting sections
    :return: Cell configuration report
    """
    query = CommonSectionsOnlyQuery(sections)
    response_dict = Sender.get('tmp/c%s' % query())
    return handle_response(response_dict, 'rc')
