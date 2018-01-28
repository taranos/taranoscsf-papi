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


from taranoscsfpapi.api import *


class SignalModes:
    Continuous = 1
    Discrete = 2


def check_mode_arg(mode):
    if mode == SignalModes.Continuous:
        return 'c'
    elif mode == SignalModes.Discrete:
        return 'd'
    else:
        raise PapiException(-1, 'mode arg invalid')


def tk(new_value=None):
    if new_value:
        Globals.tk = new_value
    return Globals.tk


#
# Signal Trunk:
#

# Create:

class TrunkConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)

    def __call__(self):
        request_dict = {
            'm': {
                't': self.tag}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        return request_dict


def create_trunks(*, constructors):
    response_dict = Sender.put(constructors, 'ct', 'tsp/t', method='POST')
    return handle_response(response_dict, 'rt')


def create_trunk(**kwargs):
    return create_trunks(constructors=[TrunkConstructor(**kwargs)])[0]


# Destroy:

class TrunkDestructor:
    def __init__(self,
                 key,
                 scope=None):
        self.key = check_key_arg(key)
        self.scope = check_string_arg(scope)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        return request_dict


def destroy_trunks(*, destructors):
    response_dict = Sender.put(destructors, 'dt', 'tsp/t', method='DELETE')
    return handle_response(response_dict, None)


def destroy_trunk(*, key=None, **kwargs):
    if not key:
        key = tk()
    return destroy_trunks(destructors=[TrunkDestructor(key, **kwargs)])


# Report:

class TrunkQuery(CommonQuery):
    pass


def report_trunks(*, keys, sections=None):
    query = TrunkQuery(keys, sections)
    response_dict = Sender.get('tsp/t%s' % query())
    return handle_response(response_dict, 'rt')


def report_trunk(*, key=None, sections=None):
    if not key:
        key = tk()
    result = report_trunks(keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class TrunkUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        return request_dict


def update_trunks(*, updates):
    response_dict = Sender.put(updates, 'ut', 'tsp/t')
    return handle_response(response_dict, None)


def update_trunk(*, key=None, **kwargs):
    if not key:
        key = tk()
    return update_trunks(updates=[TrunkUpdate(key, **kwargs)])


#
# Signal Interface:
#

# Create:

class SignalInterfaceConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)

    def __call__(self):
        request_dict = {
            'm': {
                't': self.tag}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        return request_dict

        
def create_signal_interfaces(*, trunk_key=None, constructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(constructors, 'csi', 'tsp/t/%s/si' % trunk_key, method='POST')
    return handle_response(response_dict, 'rsi')


def create_signal_interface(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return create_signal_interfaces(trunk_key=trunk_key,
                                    constructors=[SignalInterfaceConstructor(**kwargs)])[0]


# Destroy:

class SignalInterfaceDestructor:
    def __init__(self,
                 key):
        self.key = check_key_arg(key)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        return request_dict

        
def destroy_signal_interfaces(*, trunk_key=None, destructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(destructors, 'dsi', 'tsp/t/%s/si' % trunk_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_signal_interface(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return destroy_signal_interfaces(trunk_key=trunk_key,
                                     destructors=[SignalInterfaceDestructor(**kwargs)])


# Report:

class SignalInterfaceQuery(CommonQuery):
    pass


def report_signal_interfaces(*, trunk_key=None, keys, sections=None):
    if not trunk_key:
        trunk_key = tk()
    query = SignalInterfaceQuery(keys, sections)
    response_dict = Sender.get('tsp/t/%s/si%s' % (trunk_key, query()))
    return handle_response(response_dict, 'rsi')


def report_signal_interface(*, trunk_key=None, key, sections=None):
    if not trunk_key:
        trunk_key = tk()
    result = report_signal_interfaces(trunk_key=trunk_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SignalInterfaceUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        return request_dict


def update_signal_interfaces(*, trunk_key=None, updates):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(updates, 'usi', 'tsp/t/%s/si' % trunk_key)
    return handle_response(response_dict, None)


def update_signal_interface(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return update_signal_interfaces(trunk_key=trunk_key, updates=[SignalInterfaceUpdate(**kwargs)])


#
# Signal Port:
#

# Create:

class SignalPortConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 alias=None,
                 mode=SignalModes.Continuous):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.alias = check_string_arg(alias)
        self.mode = check_mode_arg(mode)

    def __call__(self):
        request_dict = {
            'm': {
                't': self.tag}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.alias:
            request_dict['m']['a'] = self.alias
        request_dict['m']['m'] = self.mode
        return request_dict


def create_signal_ports(*, trunk_key=None, interface_key, constructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(
        constructors, 'csp', 'tsp/t/%s/si/%s/sp' % (trunk_key, interface_key), method='POST')
    return handle_response(response_dict, 'rsp')


def create_signal_port(*, trunk_key=None, interface_key, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return create_signal_ports(trunk_key=trunk_key,
                               interface_key=interface_key,
                               constructors=[SignalPortConstructor(**kwargs)])[0]


# Destroy:

class SignalPortDestructor:
    def __init__(self,
                 key):
        self.key = key

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        return request_dict


def destroy_signal_ports(*, trunk_key=None, destructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(destructors, 'dsp', 'tsp/t/%s/sp' % trunk_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_signal_port(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return destroy_signal_ports(trunk_key=trunk_key, destructors=[SignalPortDestructor(**kwargs)])


# Lookup:

def lookup_signal_port(*, trunk_key=None, alias):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.get('tsp/t/%s/spa/%s' % (trunk_key, alias))
    return handle_response(response_dict, 'lsp')


# Report:

class SignalPortQuery(CommonQuery):
    pass


def report_signal_ports(*, trunk_key=None, interface_key, keys, sections=None):
    if not trunk_key:
        trunk_key = tk()
    query = SignalPortQuery(keys, sections)
    response_dict = Sender.get('tsp/t/%s/si/%s/sp%s' % (trunk_key, interface_key, query()))
    return handle_response(response_dict, 'rsp')


def report_signal_port(*, trunk_key=None, interface_key, key, sections=None):
    if not trunk_key:
        trunk_key = tk()
    result = report_signal_ports(trunk_key=trunk_key,
                                 interface_key=interface_key,
                                 keys=[key],
                                 sections=sections)
    return None if not result else result[0]


# Update:

class SignalPortUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 alias=None,
                 signal=None):
        self.key = check_string_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.alias = check_string_arg(alias)
        self.signal = check_string_arg(signal)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.alias:
            request_dict['m']['a'] = self.alias
        if self.signal:
            request_dict['s'] = {}
            request_dict['s']['s'] = self.signal
        return request_dict


def update_signal_ports(*, trunk_key=None, updates):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(updates, 'usp', 'tsp/t/%s/sp' % trunk_key)
    return handle_response(response_dict, None)


def update_signal_port(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return update_signal_ports(trunk_key=trunk_key, updates=[SignalPortUpdate(**kwargs)])


#
# Signal Source:
#

# Create:

class SignalSourceConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)

    def __call__(self):
        request_dict = {
            'm': {
                't': self.tag}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        return request_dict


def create_signal_sources(*, trunk_key=None, constructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(constructors, 'css', 'tsp/t/%s/ss' % trunk_key, method='POST')
    return handle_response(response_dict, 'rss')


def create_signal_source(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return create_signal_sources(trunk_key=trunk_key, constructors=[SignalSourceConstructor(**kwargs)])[0]


# Destroy:

class SignalSourceDestructor:
    def __init__(self,
                 key):
        self.key = check_key_arg(key)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        return request_dict


def destroy_signal_sources(*, trunk_key=None, destructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(destructors, 'dss', 'tsp/t/%s/ss' % trunk_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_signal_source(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return destroy_signal_sources(trunk_key=trunk_key, destructors=[SignalSourceDestructor(**kwargs)])


# Report:

class SignalSourceQuery(CommonQuery):
    pass


def report_signal_sources(*, trunk_key=None, keys, sections=None):
    if not trunk_key:
        trunk_key = tk()
    query = SignalSourceQuery(keys, sections)
    response_dict = Sender.get('tsp/t/%s/ss%s' % (trunk_key, query()))
    return handle_response(response_dict, 'rss')


def report_signal_source(*, trunk_key=None, key, sections=None):
    if not trunk_key:
        trunk_key = tk()
    result = report_signal_sources(trunk_key=trunk_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SignalSourceUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 signal=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.signal = check_string_arg(signal)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.signal:
            request_dict['s'] = {}
            request_dict['s']['s'] = self.signal
        return request_dict


def update_signal_sources(*, trunk_key=None, updates):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(updates, 'uss', 'tsp/t/%s/ss' % trunk_key)
    return handle_response(response_dict, None)


def update_signal_source(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return update_signal_sources(trunk_key=trunk_key, updates=[SignalSourceUpdate(**kwargs)])


#
# Signal Sink:
#

# Create:

class SignalSinkConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 mode=SignalModes.Continuous):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.mode = check_mode_arg(mode)

    def __call__(self):
        request_dict = {
            'm': {
                't': self.tag}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        request_dict['m']['m'] = self.mode
        return request_dict


def create_signal_sinks(*, trunk_key=None, constructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(constructors, 'csk', 'tsp/t/%s/sk' % trunk_key, method='POST')
    return handle_response(response_dict, 'rsk')


def create_signal_sink(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return create_signal_sinks(trunk_key=trunk_key, constructors=[SignalSinkConstructor(**kwargs)])[0]


# Destroy:

class SignalSinkDestructor:
    def __init__(self,
                 key):
        self.key = check_key_arg(key)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        return request_dict


def destroy_signal_sinks(*, trunk_key=None, destructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(destructors, 'dsk', 'tsp/t/%s/sk' % trunk_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_signal_sink(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return destroy_signal_sinks(trunk_key=trunk_key, destructors=[SignalSinkDestructor(**kwargs)])


# Report:

class SignalSinkQuery(CommonQuery):
    pass


def report_signal_sinks(*, trunk_key=None, keys, sections=None):
    if not trunk_key:
        trunk_key = tk()
    query = SignalSinkQuery(keys, sections)
    response_dict = Sender.get('tsp/t/%s/sk%s' % (trunk_key, query()))
    return handle_response(response_dict, 'rsk')


def report_signal_sink(*, trunk_key=None, key, sections=None):
    if not trunk_key:
        trunk_key = tk()
    result = report_signal_sinks(trunk_key=trunk_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SignalSinkUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 signal=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.signal = check_string_arg(signal)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.signal:
            request_dict['s'] = {}
            request_dict['s']['s'] = self.signal
        return request_dict


def update_signal_sinks(*, trunk_key=None, updates):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(updates, 'usk', 'tsp/t/%s/sk' % trunk_key)
    return handle_response(response_dict, None)


def update_signal_sink(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return update_signal_sinks(trunk_key=trunk_key, updates=[SignalSinkUpdate(**kwargs)])


#
# Signal Link:
#

# Create:

class SignalLinkConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 mode=SignalModes.Continuous,
                 source_key=None,
                 sink_key=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.mode = check_mode_arg(mode)
        self.sink_key = check_key_arg(sink_key)
        self.source_key = check_key_arg(source_key)

    def __call__(self):
        request_dict = {
            'm': {
                't': self.tag},
            'r': {
                'sk': self.sink_key,
                'ss': self.source_key}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        request_dict['m']['m'] = self.mode
        return request_dict

        
def create_signal_links(*, trunk_key=None, constructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(constructors, 'csl', 'tsp/t/%s/sl' % trunk_key, method='POST')
    return handle_response(response_dict, 'rsl')


def create_signal_link(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return create_signal_links(trunk_key=trunk_key, constructors=[SignalLinkConstructor(**kwargs)])[0]


# Destroy:

class SignalLinkDestructor:
    def __init__(self,
                 key):
        self.key = check_key_arg(key)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        return request_dict

        
def destroy_signal_links(*, trunk_key=None, destructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(destructors, 'dsl', 'tsp/t/%s/sl' % trunk_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_signal_link(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return destroy_signal_links(trunk_key=trunk_key, destructors=[SignalLinkDestructor(**kwargs)])


# Report:

class SignalLinkQuery(CommonQuery):
    pass


def report_signal_links(*, trunk_key=None, keys, sections=None):
    if not trunk_key:
        trunk_key = tk()
    query = SignalLinkQuery(keys, sections)
    response_dict = Sender.get('tsp/t/%s/sl%s' % (trunk_key, query()))
    return handle_response(response_dict, 'rsl')


def report_signal_link(*, trunk_key=None, key, sections=None):
    if not trunk_key:
        trunk_key = tk()
    result = report_signal_links(trunk_key=trunk_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SignalLinkUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        return request_dict


def update_signal_links(*, trunk_key=None, updates):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(updates, 'usl', 'tsp/t/%s/sl' % trunk_key)
    return handle_response(response_dict, None)


def update_signal_link(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return update_signal_links(trunk_key=trunk_key, updates=[SignalLinkUpdate(**kwargs)])


#
# Signal Tap:
#

# Create:

class SignalTapConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 mode=SignalModes.Continuous):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.mode = check_mode_arg(mode)

    def __call__(self):
        request_dict = {
            'm': {
                't': self.tag}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        request_dict['m']['m'] = self.mode
        return request_dict

        
def create_signal_taps(*, trunk_key=None, constructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(constructors, 'cst', 'tsp/t/%s/st' % trunk_key, method='POST')
    return handle_response(response_dict, 'rst')


def create_signal_tap(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return create_signal_taps(trunk_key=trunk_key, constructors=[SignalTapConstructor(**kwargs)])[0]


# Destroy:

class SignalTapDestructor:
    def __init__(self,
                 key):
        self.key = check_key_arg(key)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        return request_dict


def destroy_signal_taps(*, trunk_key=None, destructors=None):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(destructors, 'dst', 'tsp/t/%s/st' % trunk_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_signal_tap(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return destroy_signal_taps(trunk_key=trunk_key, destructors=[SignalTapDestructor(**kwargs)])


# Report:

class SignalTapQuery(CommonQuery):
    pass


def report_signal_taps(*, trunk_key=None, keys, sections=None):
    if not trunk_key:
        trunk_key = tk()
    query = SignalTapQuery(keys, sections)
    response_dict = Sender.get('tsp/t/%s/st%s' % (trunk_key, query()))
    return handle_response(response_dict, 'rst')


def report_signal_tap(*, trunk_key=None, key, sections=None):
    if not trunk_key:
        trunk_key = tk()
    result = report_signal_taps(trunk_key=trunk_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SignalTapUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 signal=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.signal = check_string_arg(signal)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.signal:
            if 's' not in request_dict:
                request_dict['s'] = {}
            request_dict['s']['s'] = self.signal
        return request_dict


def update_signal_taps(*, trunk_key=None, updates):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(updates, 'ust', 'tsp/t/%s/st' % trunk_key)
    return handle_response(response_dict, None)


def update_signal_tap(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return update_signal_taps(trunk_key=trunk_key, updates=[SignalTapUpdate(**kwargs)])


#
# Signal Input:
#

# Create:

class SignalInputConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 mode=SignalModes.Continuous):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.mode = check_mode_arg(mode)

    def __call__(self):
        request_dict = {
            'm': {
                't': self.tag}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        request_dict['m']['m'] = self.mode
        return request_dict

        
def create_signal_inputs(*, trunk_key=None, constructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(constructors, 'csmi', 'tsp/t/%s/smi' % trunk_key, method='POST')
    return handle_response(response_dict, 'rsmi')


def create_signal_input(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return create_signal_inputs(trunk_key=trunk_key, constructors=[SignalInputConstructor(**kwargs)])[0]


# Destroy:

class SignalInputDestructor:
    def __init__(self,
                 key):
        self.key = check_key_arg(key)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        return request_dict

        
def destroy_signal_inputs(*, trunk_key=None, destructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(destructors, 'dsmi', 'tsp/t/%s/smi' % trunk_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_signal_input(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return destroy_signal_inputs(trunk_key=trunk_key, destructors=[SignalInputDestructor(**kwargs)])


# Report:

class SignalInputQuery(CommonQuery):
    pass


def report_signal_inputs(*, trunk_key=None, keys, sections=None):
    if not trunk_key:
        trunk_key = tk()
    query = SignalInputQuery(keys, sections)
    response_dict = Sender.get('tsp/t/%s/smi%s' % (trunk_key, query()))
    return handle_response(response_dict, 'rsmi')


def report_signal_input(*, trunk_key=None, key, sections=None):
    if not trunk_key:
        trunk_key = tk()
    result = report_signal_inputs(trunk_key=trunk_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SignalInputUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 signal=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.signal = check_string_arg(signal)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.signal:
            request_dict['s'] = {}
            request_dict['s']['s'] = self.signal
        return request_dict


def update_signal_inputs(*, trunk_key=None, updates):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(updates, 'usmi', 'tsp/t/%s/smi' % trunk_key)
    return handle_response(response_dict, None)


def update_signal_input(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return update_signal_inputs(trunk_key=trunk_key, updates=[SignalInputUpdate(**kwargs)])


#
# Signal Bridge:
#

# Create:

class SignalBridgeConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 mode=SignalModes.Continuous,
                 modulatable_key=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.mode = check_mode_arg(mode)
        self.modulatable_key = check_key_arg(modulatable_key)

    def __call__(self):
        request_dict = {
            'm': {
                't': self.tag}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        request_dict['m']['m'] = self.mode
        if self.modulatable_key:
            request_dict['r'] = {}
            request_dict['r']['sm'] = self.modulatable_key
        return request_dict

        
def create_signal_bridges(*, trunk_key=None, constructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(constructors, 'csmb', 'tsp/t/%s/smb' % trunk_key, method='POST')
    return handle_response(response_dict, 'rsmb')


def create_signal_bridge(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return create_signal_bridges(trunk_key=trunk_key, constructors=[SignalBridgeConstructor(**kwargs)])[0]


# Destroy:

class SignalBridgeDestructor:
    def __init__(self,
                 key):
        self.key = check_key_arg(key)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        return request_dict

        
def destroy_signal_bridges(*, trunk_key=None, destructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(destructors, 'dsmb', 'tsp/t/%s/smb' % trunk_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_signal_bridge(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return destroy_signal_bridges(trunk_key=trunk_key, destructors=[SignalBridgeDestructor(**kwargs)])


# Report:

class SignalBridgeQuery(CommonQuery):
    pass


def report_signal_bridges(*, trunk_key=None, keys, sections=None):
    if not trunk_key:
        trunk_key = tk()
    query = SignalBridgeQuery(keys, sections)
    response_dict = Sender.get('tsp/t/%s/smb%s' % (trunk_key, query()))
    return handle_response(response_dict, 'rsmb')


def report_signal_bridge(*, trunk_key=None, key, sections=None):
    if not trunk_key:
        trunk_key = tk()
    result = report_signal_bridges(trunk_key=trunk_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SignalBridgeUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 signal=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.signal = check_string_arg(signal)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.signal:
            request_dict['s'] = {}
            request_dict['s']['s'] = self.signal
        return request_dict


def update_signal_bridges(*, trunk_key=None, updates):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(updates, 'usmb', 'tsp/t/%s/smb' % trunk_key)
    return handle_response(response_dict, None)


def update_signal_bridge(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return update_signal_bridges(trunk_key=trunk_key, updates=[SignalBridgeUpdate(**kwargs)])


#
# Signal Output:
#

# Create:

class SignalOutputConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 mode=SignalModes.Continuous,
                 modulatable_key=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.mode = check_mode_arg(mode)
        self.modulatable_key = check_key_arg(modulatable_key)

    def __call__(self):
        request_dict = {
            'm': {
                't': self.tag}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        request_dict['m']['m'] = self.mode
        if self.modulatable_key:
            request_dict['r'] = {}
            request_dict['r']['sm'] = self.modulatable_key
        return request_dict

        
def create_signal_outputs(*, trunk_key=None, constructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(constructors, 'csmo', 'tsp/t/%s/smo' % trunk_key, method='POST')
    return handle_response(response_dict, 'rsmo')


def create_signal_output(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return create_signal_outputs(trunk_key=trunk_key, constructors=[SignalOutputConstructor(**kwargs)])[0]


# Destroy:

class SignalOutputDestructor:
    def __init__(self,
                 key):
        self.key = check_key_arg(key)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        return request_dict

        
def destroy_signal_outputs(*, trunk_key=None, destructors):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(destructors, 'dsmo', 'tsp/t/%s/smo' % trunk_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_signal_output(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return destroy_signal_outputs(trunk_key=trunk_key, destructors=[SignalOutputDestructor(**kwargs)])


# Report:

class SignalOutputQuery(CommonQuery):
    pass


def report_signal_outputs(*, trunk_key=None, keys, sections=None):
    if not trunk_key:
        trunk_key = tk()
    query = SignalOutputQuery(keys, sections)
    response_dict = Sender.get('tsp/t/%s/smo%s' % (trunk_key, query()))
    return handle_response(response_dict, 'rsmo')


def report_signal_output(*, trunk_key=None, key, sections=None):
    if not trunk_key:
        trunk_key = tk()
    result = report_signal_outputs(trunk_key=trunk_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SignalOutputUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 signal=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.signal = check_string_arg(signal)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.signal:
            request_dict['s'] = {}
            request_dict['s']['s'] = self.signal
        return request_dict


def update_signal_outputs(*, trunk_key=None, updates):
    if not trunk_key:
        trunk_key = tk()
    response_dict = Sender.put(updates, 'usmo', 'tsp/t/%s/smo' % trunk_key)
    return handle_response(response_dict, None)


def update_signal_output(*, trunk_key=None, **kwargs):
    if not trunk_key:
        trunk_key = tk()
    return update_signal_outputs(trunk_key=trunk_key, updates=[SignalOutputUpdate(**kwargs)])
