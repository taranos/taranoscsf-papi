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

def destroy_cell():
    """
    Destroy (reset) the currently associated simulation cell.

    :return: Cell destruction report
    """
    response_dict = Sender.put({}, 'dc', 'tmp/c', method='DELETE')
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
