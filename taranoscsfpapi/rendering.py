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


class DestructorScopes:
    Shallow = 's'
    Deep = 'd'


def check_envelope_def_arg(envelope_def):
    if envelope_def and type(envelope_def) is not dict:
        raise PapiException(-1, 'envelope def arg invalid')
    return envelope_def


def check_macro_arg(macro):
    if not macro or type(macro) is not dict:
        raise PapiException(-1, 'macro arg invalid')
    return macro


def check_patch_def_arg(patch_def):
    if patch_def and type(patch_def) is not dict:
        raise PapiException(-1, 'patch def arg invalid')
    return patch_def


def check_position_arg(position):
    if position:
        if (type(position) is not list or
            len(position) != 2 or
            position[0] < -1.0 or position[0] > 1.0 or
                position[1] < -1.0 or position[1] > 1.0):
                raise PapiException(-1, 'position arg invalid')
        return [str(position[0]), str(position[1])]
    else:
        return None


def check_rotation_arg(rotation):
    if rotation:
        if (type(rotation) is not list or
            len(rotation) != 1 or
                rotation[0] < -1.0 or rotation[0] > 1.0):
                raise PapiException(-1, 'rotation arg invalid')
        return [str(rotation[0])]
    else:
        return None


def check_scope_arg(scope):
    if scope:
        if scope == DestructorScopes.Deep:
            return 'd'
        elif scope == DestructorScopes.Shallow:
            return 's'
        else:
            raise PapiException(-1, 'scope arg invalid')
    else:
        return None


def fk(new_value=None):
    """
    Get/set the default field key.

    :param new_value: New default field key
    :return: Current default field key
    """
    if new_value:
        Globals.fk = new_value
    return Globals.fk


#
# Field:
#

# Create:

class FieldConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 acoustic_c=None,
                 acoustic_rho=None,
                 antipode_distance=None,
                 geometry=None,
                 trunk_key=None,
                 modulator_key=None,
                 patch_def=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.acoustic_c = check_real_arg(acoustic_c)
        self.acoustic_rho = check_real_arg(acoustic_rho)
        self.antipode_distance = check_real_arg(antipode_distance)
        self.geometry = check_string_arg(geometry)
        self.trunk_key = check_key_arg(trunk_key)
        self.modulator_key = check_key_arg(modulator_key)
        self.patch_def = check_patch_def_arg(patch_def)

    def __call__(self):
        request_dict = {
            'm': {'t': self.tag}}
        if self.badge:
            request_dict['m']['b'] = self.badge
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.acoustic_c:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['ac'] = self.acoustic_c
        if self.acoustic_rho:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['ar'] = self.acoustic_rho
        if self.antipode_distance:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['ad'] = self.antipode_distance
        if self.geometry:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['g'] = self.geometry
        if self.patch_def:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['dpe'] = self.patch_def
        if self.modulator_key:
            if 'r' not in request_dict:
                request_dict['r'] = {}
            request_dict['r']['sm'] = self.modulator_key
        if self.trunk_key:
            if 'r' not in request_dict:
                request_dict['r'] = {}
            request_dict['r']['t'] = self.trunk_key
        return request_dict


def create_fields(*, constructors):
    """
    Create new fields.

    :param constructors: Field constructor list
    :return: Field creation reports
    """
    response_dict = Sender.put(constructors, 'cf', 'trp/f', method='POST')
    return handle_response(response_dict, 'rf')


def create_field(**kwargs):
    """
    Create a new field.

    :param kwargs: Field constructor arguments
    :return: Field creation report
    """
    return create_fields(constructors=[FieldConstructor(**kwargs)])[0]


# Destroy:

class FieldDestructor:
    def __init__(self,
                 key,
                 scope=None):
        self.key = check_key_arg(key)
        self.scope = check_scope_arg(scope)

    def __call__(self):
        request_dict = {
            'm': {'k': self.key}}
        if self.scope:
            request_dict['s'] = self.scope
        return request_dict


def destroy_fields(*, destructors):
    """
    Destroy fields.

    :param destructors: Field destructor list
    :return: Field destruction reports
    """
    response_dict = Sender.put(destructors, 'df', 'trp/f', method='DELETE')
    return handle_response(response_dict, None)


def destroy_field(*, key=None, **kwargs):
    """
    Destroy a field.

    :param key: Field key
    :param kwargs: Field destructor arguments
    :return: Field destruction report
    """
    if not key:
        key = fk()
    return destroy_fields(destructors=[FieldDestructor(key, **kwargs)])


# Report:

class FieldQuery(CommonQuery):
    pass


def report_fields(*, keys, sections=None):
    query = FieldQuery(keys, sections)
    response_dict = Sender.get('trp/f%s' % query())
    return handle_response(response_dict, 'rf')


def report_field(*, key=None, sections=None):
    if not key:
        key = fk()
    result = report_fields(keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class FieldUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 probe_updates=None,
                 subject_updates=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        if probe_updates and type(probe_updates) is not list:
            raise PapiException(-1, 'probe updates arg invalid')
        self.probe_updates = probe_updates
        if subject_updates and type(subject_updates) is not list:
            raise PapiException(-1, 'subject updates arg invalid')
        self.subject_updates = subject_updates

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.probe_updates:
            request_dict['up'] = self.probe_updates
        if self.subject_updates:
            request_dict['us'] = self.subject_updates
        return request_dict


def update_fields(*, updates):
    response_dict = Sender.put(updates, 'uf', 'trp/f')
    return handle_response(response_dict, None)


def update_field(*, key=None, **kwargs):
    if not key:
        key = fk()
    return update_fields(updates=[FieldUpdate(key, **kwargs)])


#
# Field Emitter:
#

# Create:

class FieldEmitterConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 modulator_key=None,
                 patch_def=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.modulator_key = check_key_arg(modulator_key)
        self.patch_def = check_patch_def_arg(patch_def)

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
        if self.patch_def:
            request_dict['a'] = {'dpe': self.patch_def}
        if self.modulator_key:
            request_dict['r'] = {'sm': self.modulator_key}
        return request_dict


def create_field_emitters(*, field_key=None, constructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(constructors, 'cfe', 'trp/f/%s/fe' % field_key, method='POST')
    return handle_response(response_dict, 'rfe')


def create_field_emitter(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return create_field_emitters(field_key=field_key, constructors=[FieldEmitterConstructor(**kwargs)])[0]


# Destroy:

class FieldEmitterDestructor:
    def __init__(self,
                 key,
                 scope=None):
        self.key = check_key_arg(key)
        self.scope = check_scope_arg(scope)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.scope:
            request_dict['s'] = self.scope
        return request_dict


def destroy_field_emitters(*, field_key=None, destructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(destructors, 'dfe', 'trp/f/%s/fe' % field_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_field_emitter(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return destroy_field_emitters(field_key=field_key, destructors=[FieldEmitterDestructor(**kwargs)])


# Report:

class FieldEmitterQuery(CommonQuery):
    pass


def report_field_emitters(*, field_key=None, keys, sections=None):
    if not field_key:
        field_key = fk()
    query = FieldEmitterQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/fe%s' % (field_key, query()))
    return handle_response(response_dict, 'rfe')


def report_field_emitter(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_field_emitters(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class FieldEmitterUpdate:
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


def update_field_emitters(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'ufe', 'trp/f/%s/fe' % field_key)
    return handle_response(response_dict, None)


def update_field_emitter(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_field_emitters(field_key=field_key, updates=[FieldEmitterUpdate(**kwargs)])


# Call:

class FieldEmitterCall:
    def __init__(self,
                 key,
                 macro):
        self.key = check_key_arg(key)
        self.macro = check_macro_arg(macro)

    def __call__(self):
        request_dict = {
            'k': self.key,
            'm': self.macro}
        return request_dict


def call_field_emitters(*, field_key=None, calls):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(calls, 'mfe', 'trp/f/%s/fe/m' % field_key)
    return handle_response(response_dict, None)


def call_field_emitter(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return call_field_emitters(field_key=field_key, calls=[FieldEmitterCall(**kwargs)])


#
# Field Oscillator:
#

# Report:

class FieldOscillatorQuery(CommonQuery):
    pass


def report_field_oscillators(*, field_key=None, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = FieldOscillatorQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/fo%s' % (field_key, query()))
    return handle_response(response_dict, 'rfo')


def report_field_oscillators_of_emitter(*, field_key=None, emitter_key, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = FieldOscillatorQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/fe/%s/fo%s' % (field_key, emitter_key, query()))
    return handle_response(response_dict, 'rfo')


def report_field_oscillator(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_field_oscillators(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class FieldOscillatorUpdate:
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


def update_field_oscillators(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'ufo', 'trp/f/%s/fo' % field_key)
    return handle_response(response_dict, None)


def update_field_oscillator(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_field_oscillators(field_key=field_key, updates=[FieldOscillatorUpdate(**kwargs)])


# Call:

class FieldOscillatorCall:
    def __init__(self,
                 key,
                 macro):
        self.key = check_key_arg(key)
        self.macro = check_macro_arg(macro)

    def __call__(self):
        request_dict = {
            'k': self.key,
            'm': self.macro}
        return request_dict


def call_field_oscillators(*, field_key=None, calls):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(calls, 'mfo', 'trp/f/%s/fo/m' % field_key)
    return handle_response(response_dict, None)


def call_field_oscillator(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return call_field_oscillators(field_key=field_key, calls=[FieldOscillatorCall(**kwargs)])


#
# Subject:
#

# Create:

class SubjectConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 modulator_key=None,
                 patch_def=None,
                 position=None,
                 rotation=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.modulator_key = check_key_arg(modulator_key)
        self.patch_def = check_patch_def_arg(patch_def)
        self.position = check_position_arg(position)
        self.rotation = check_rotation_arg(rotation)

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
        if self.patch_def:
            request_dict['a'] = {'dpe': self.patch_def}
        if self.modulator_key:
            request_dict['r'] = {'sm': self.modulator_key}
        if self.position:
            if 's' not in request_dict:
                request_dict['s'] = {}
            request_dict['s']['p'] = self.position
        if self.rotation:
            if 's' not in request_dict:
                request_dict['s'] = {}
            request_dict['s']['r'] = self.rotation
        return request_dict


def create_subjects(*, field_key=None, constructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(constructors, 'cs', 'trp/f/%s/s' % field_key, method='POST')
    return handle_response(response_dict, 'rs')


def create_subject(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return create_subjects(field_key=field_key, constructors=[SubjectConstructor(**kwargs)])[0]


# Destroy:

class SubjectDestructor:
    def __init__(self,
                 key,
                 scope=None):
        self.key = check_key_arg(key)
        self.scope = check_scope_arg(scope)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.scope:
            request_dict['s'] = self.scope
        return request_dict


def destroy_subjects(*, field_key=None, destructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(destructors, 'ds', 'trp/f/%s/s' % field_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_subject(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return destroy_subjects(field_key=field_key, destructors=[SubjectDestructor(**kwargs)])


# Report:

class SubjectQuery(CommonQuery):
    pass


def report_subjects(*, field_key=None, keys, sections=None):
    if not field_key:
        field_key = fk()
    query = SubjectQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/s%s' % (field_key, query()))
    return handle_response(response_dict, 'rs')


def report_subject(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_subjects(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SubjectUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 position=None,
                 rotation=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.position = check_position_arg(position)
        self.rotation = check_rotation_arg(rotation)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.position:
            if 's' not in request_dict:
                request_dict['s'] = {}
            request_dict['s']['p'] = self.position
        if self.rotation:
            if 's' not in request_dict:
                request_dict['s'] = {}
            request_dict['s']['r'] = self.rotation
        return request_dict


def update_subjects(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'us', 'trp/f/%s/s' % field_key)
    return handle_response(response_dict, None)


def update_subject(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_subjects(field_key=field_key, updates=[SubjectUpdate(**kwargs)])


#
# Subject Emitter:
#

# Create:

class SubjectEmitterConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 modulator_key=None,
                 patch_def=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.modulator_key = check_key_arg(modulator_key)
        self.patch_def = check_patch_def_arg(patch_def)

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
        if self.patch_def:
            request_dict['a'] = {'dpe': self.patch_def}
        if self.modulator_key:
            request_dict['r'] = {'sm': self.modulator_key}
        return request_dict


def create_subject_emitters(*, field_key=None, subject_key, constructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(
        constructors, 'cse', 'trp/f/%s/s/%s/se' % (field_key, subject_key), method='POST')
    return handle_response(response_dict, 'rse')


def create_subject_emitter(*, field_key=None, subject_key, **kwargs):
    if not field_key:
        field_key = fk()
    return create_subject_emitters(field_key=field_key,
                                   subject_key=subject_key,
                                   constructors=[SubjectEmitterConstructor(**kwargs)])[0]


# Destroy:

class SubjectEmitterDestructor:
    def __init__(self,
                 key,
                 scope=None):
        self.key = check_key_arg(key)
        self.scope = check_scope_arg(scope)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.scope:
            request_dict['s'] = self.scope
        return request_dict


def destroy_subject_emitters(*, field_key=None, destructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(destructors, 'dse', 'trp/f/%s/se' % field_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_subject_emitter(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return destroy_subject_emitters(field_key=field_key, destructors=[SubjectEmitterDestructor(**kwargs)])


# Report:

class SubjectEmitterQuery(CommonQuery):
    pass


def report_subject_emitters(*, field_key=None, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = SubjectEmitterQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/se%s' % (field_key, query()))
    return handle_response(response_dict, 'rse')


def report_subject_emitters_of_subject(*, field_key=None, subject_key, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = SubjectEmitterQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/s/%s/se%s' % (field_key, subject_key, query()))
    return handle_response(response_dict, 'rse')


def report_subject_emitter(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_subject_emitters(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SubjectEmitterUpdate:
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


def update_subject_emitters(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'use', 'trp/f/%s/se' % field_key)
    return handle_response(response_dict, None)


def update_subject_emitter(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_subject_emitters(field_key=field_key, updates=[SubjectEmitterUpdate(**kwargs)])


# Call:

class SubjectEmitterCall:
    def __init__(self,
                 key,
                 macro):
        self.key = check_key_arg(key)
        self.macro = check_macro_arg(macro)

    def __call__(self):
        request_dict = {
            'k': self.key,
            'm': self.macro}
        return request_dict


def call_subject_emitters(*, field_key=None, calls):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(calls, 'mse', 'trp/f/%s/se/m' % field_key)
    return handle_response(response_dict, None)


def call_subject_emitter(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return call_subject_emitters(field_key=field_key, calls=[SubjectEmitterCall(**kwargs)])


#
# Subject Oscillator:
#

# Report:

class SubjectOscillatorQuery(CommonQuery):
    pass


def report_subject_oscillators(*, field_key=None, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = SubjectOscillatorQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/so%s' % (field_key, query()))
    return handle_response(response_dict, 'rso')


def report_subject_oscillators_of_emitter(*, field_key=None, emitter_key, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = SubjectOscillatorQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/se/%s/so%s' % (field_key, emitter_key, query()))
    return handle_response(response_dict, 'rso')


def report_subject_oscillator(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_subject_oscillators(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class SubjectOscillatorUpdate:
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


def update_subject_oscillators(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'uso', 'trp/f/%s/so' % field_key)
    return handle_response(response_dict, None)


def update_subject_oscillator(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_subject_oscillators(field_key=field_key, updates=[SubjectOscillatorUpdate(**kwargs)])


# Call:

class SubjectOscillatorCall:
    def __init__(self,
                 key,
                 macro):
        self.key = check_key_arg(key)
        self.macro = check_macro_arg(macro)

    def __call__(self):
        request_dict = {
            'k': self.key,
            'm': self.macro}
        return request_dict


def call_subject_oscillators(*, field_key=None, calls):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(calls, 'mso', 'trp/f/%s/so/m' % field_key)
    return handle_response(response_dict, None)


def call_subject_oscillator(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return call_subject_oscillators(field_key=field_key, calls=[SubjectOscillatorCall(**kwargs)])


#
# Probe:
#

# Create:

class ProbeConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 position=None,
                 rotation=None,
                 acoustic_a=None,
                 squelch_threshold=None,
                 lobe_range=None,
                 lobe_range_poles=None,
                 lobe_bearing_poles=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.position = check_position_arg(position)
        self.rotation = check_rotation_arg(rotation)
        self.acoustic_a = check_real_arg(acoustic_a)
        self.squelch_threshold = check_real_arg(squelch_threshold)
        self.lobe_range = check_real_arg(lobe_range)
        self.lobe_range_poles = check_string_arg(lobe_range_poles)
        self.lobe_bearing_poles = check_string_arg(lobe_bearing_poles)

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
        if self.acoustic_a:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['aa'] = self.acoustic_a
        if self.squelch_threshold:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['st'] = self.squelch_threshold
        if self.lobe_range:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['lr'] = self.lobe_range
        if self.lobe_range_poles:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['lrp'] = self.lobe_range_poles
        if self.lobe_bearing_poles:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['lbp'] = self.lobe_bearing_poles
        if self.position:
            if 's' not in request_dict:
                request_dict['s'] = {}
            request_dict['s']['p'] = self.position
        if self.rotation:
            if 's' not in request_dict:
                request_dict['s'] = {}
            request_dict['s']['r'] = self.rotation
        return request_dict


def create_probes(*, field_key=None, constructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(constructors, 'cp', 'trp/f/%s/p' % field_key, method='POST')
    return handle_response(response_dict, 'rp')


def create_probe(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return create_probes(field_key=field_key, constructors=[ProbeConstructor(**kwargs)])[0]


# Destroy:

class ProbeDestructor:
    def __init__(self,
                 key,
                 scope=None):
        self.key = check_key_arg(key)
        self.scope = check_scope_arg(scope)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.scope:
            request_dict['s'] = self.scope
        return request_dict

  
def destroy_probes(*, field_key=None, destructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(destructors, 'dp', 'trp/f/%s/p' % field_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_probe(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return destroy_probes(field_key=field_key, destructors=[ProbeDestructor(**kwargs)])


# Report:

class ProbeQuery(CommonQuery):
    pass


def report_probes(*, field_key=None, keys, sections=None):
    if not field_key:
        field_key = fk()
    query = ProbeQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/p%s' % (field_key, query()))
    return handle_response(response_dict, 'rp')


def report_probe(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_probes(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class ProbeUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 position=None,
                 rotation=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.position = check_position_arg(position)
        self.rotation = check_rotation_arg(rotation)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.position:
            if 's' not in request_dict:
                request_dict['s'] = {}
            request_dict['s']['p'] = self.position
        if self.rotation:
            if 's' not in request_dict:
                request_dict['s'] = {}
            request_dict['s']['r'] = self.rotation
        return request_dict


def update_probes(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'up', 'trp/f/%s/p' % field_key)
    return handle_response(response_dict, None)


def update_probe(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_probes(field_key=field_key, updates=[ProbeUpdate(**kwargs)])


#
# Probe Emitter:
#

# Create:

class ProbeEmitterConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 modulator_key=None,
                 patch_def=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.modulator_key = check_key_arg(modulator_key)
        self.patch_def = check_patch_def_arg(patch_def)

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
        if self.patch_def:
            request_dict['a'] = {'dpe': self.patch_def}
        if self.modulator_key:
            request_dict['r'] = {'sm': self.modulator_key}
        return request_dict


def create_probe_emitters(*, field_key=None, probe_key, constructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(
        constructors, 'cpe', 'trp/f/%s/p/%s/pe' % (field_key, probe_key), method='POST')
    return handle_response(response_dict, 'rpe')


def create_probe_emitter(*, field_key=None, probe_key, **kwargs):
    if not field_key:
        field_key = fk()
    return create_probe_emitters(field_key=field_key,
                                 probe_key=probe_key,
                                 constructors=[ProbeEmitterConstructor(**kwargs)])[0]


# Destroy:

class ProbeEmitterDestructor:
    def __init__(self,
                 key,
                 scope=None):
        self.key = check_key_arg(key)
        self.scope = check_scope_arg(scope)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.scope:
            request_dict['s'] = self.scope
        return request_dict


def destroy_probe_emitters(*, field_key=None, destructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(destructors, 'dpe', 'trp/f/%s/pe' % field_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_probe_emitter(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return destroy_probe_emitters(field_key=field_key, destructors=[ProbeEmitterDestructor(**kwargs)])


# Report:

class ProbeEmitterQuery(CommonQuery):
    pass


def report_probe_emitters(*, field_key=None, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = ProbeEmitterQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/pe%s' % (field_key, query()))
    return handle_response(response_dict, 'rpe')


def report_probe_emitters_of_probe(*, field_key=None, probe_key, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = ProbeEmitterQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/s/%s/pe%s' % (field_key, probe_key, query()))
    return handle_response(response_dict, 'rpe')


def report_probe_emitter(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_probe_emitters(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class ProbeEmitterUpdate:
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


def update_probe_emitters(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'upe', 'trp/f/%s/pe' % field_key)
    return handle_response(response_dict, None)


def update_probe_emitter(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_probe_emitters(field_key=field_key, updates=[ProbeEmitterUpdate(**kwargs)])


# Call:

class ProbeEmitterCall:
    def __init__(self,
                 key,
                 macro):
        self.key = check_key_arg(key)
        self.macro = check_macro_arg(macro)

    def __call__(self):
        request_dict = {
            'k': self.key,
            'm': self.macro}
        return request_dict


def call_probe_emitters(*, field_key=None, calls):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(calls, 'mse', 'trp/f/%s/se/m' % field_key)
    return handle_response(response_dict, None)


def call_probe_emitter(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return call_probe_emitters(field_key=field_key, calls=[ProbeEmitterCall(**kwargs)])


#
# Probe Oscillator:
#

# Report:

class ProbeOscillatorQuery(CommonQuery):
    pass


def report_probe_oscillators(*, field_key=None, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = ProbeOscillatorQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/po%s' % (field_key, query()))
    return handle_response(response_dict, 'rpo')


def report_probe_oscillators_of_emitter(*, field_key=None, emitter_key, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = ProbeOscillatorQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/pe/%s/po%s' % (field_key, emitter_key, query()))
    return handle_response(response_dict, 'rpo')


def report_probe_oscillator(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_probe_oscillators(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class ProbeOscillatorUpdate:
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


def update_probe_oscillators(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'upo', 'trp/f/%s/po' % field_key)
    return handle_response(response_dict, None)


def update_probe_oscillator(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_probe_oscillators(field_key=field_key, updates=[ProbeOscillatorUpdate(**kwargs)])


# Call:

class ProbeOscillatorCall:
    def __init__(self,
                 key,
                 macro):
        self.key = check_key_arg(key)
        self.macro = check_macro_arg(macro)

    def __call__(self):
        request_dict = {
            'k': self.key,
            'm': self.macro}
        return request_dict


def call_probe_oscillators(*, field_key=None, calls):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(calls, 'mpo', 'trp/f/%s/po/m' % field_key)
    return handle_response(response_dict, None)


def call_probe_oscillator(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return call_probe_oscillators(field_key=field_key, calls=[ProbeOscillatorCall(**kwargs)])


#
# Probe Collector:
#

# Create:

class ProbeCollectorConstructor:
    def __init__(self,
                 tag,
                 badge=None,
                 name=None,
                 description=None,
                 alias=None,
                 acoustic_a=None,
                 squelch_threshold=None,
                 lobe_range=None,
                 lobe_range_poles=None,
                 lobe_bearing_poles=None):
        self.tag = check_string_arg(tag)
        self.badge = check_string_arg(badge)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.alias = check_string_arg(alias)
        self.acoustic_a = check_real_arg(acoustic_a)
        self.squelch_threshold = check_real_arg(squelch_threshold)
        self.lobe_range = check_real_arg(lobe_range)
        self.lobe_range_poles = check_string_arg(lobe_range_poles)
        self.lobe_bearing_poles = check_string_arg(lobe_bearing_poles)

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
        if self.acoustic_a:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['aa'] = self.acoustic_a
        if self.squelch_threshold:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['st'] = self.squelch_threshold
        if self.lobe_range:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['lr'] = self.lobe_range
        if self.lobe_range_poles:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['lrp'] = self.lobe_range_poles
        if self.lobe_bearing_poles:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['lbp'] = self.lobe_bearing_poles
        return request_dict


def create_probe_collectors(*, field_key=None, probe_key, constructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(
        constructors, 'cpc', 'trp/f/%s/p/%s/pc' % (field_key, probe_key), method='POST')
    return handle_response(response_dict, 'rpc')


def create_probe_collector(*, field_key=None, probe_key, **kwargs):
    if not field_key:
        field_key = fk()
    return create_probe_collectors(field_key=field_key,
                                   probe_key=probe_key,
                                   constructors=[ProbeCollectorConstructor(**kwargs)])[0]


# Destroy:

class ProbeCollectorDestructor:
    def __init__(self,
                 key,
                 scope=None):
        self.key = check_key_arg(key)
        self.scope = check_scope_arg(scope)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.scope:
            request_dict['s'] = self.scope
        return request_dict


def destroy_probe_collectors(*, field_key=None, destructors):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(destructors, 'dpc', 'trp/f/%s/pc' % field_key, method='DELETE')
    return handle_response(response_dict, None)


def destroy_probe_collector(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return destroy_probe_collectors(field_key=field_key, destructors=[ProbeCollectorDestructor(**kwargs)])


# Lookup:

def lookup_probe_collector(*, field_key=None, alias):
    if not field_key:
        field_key = fk()
    response_dict = Sender.get('trp/f/%s/pc/%s' % (field_key, alias))
    return handle_response(response_dict, 'lpc')


# Report:

class ProbeCollectorQuery(CommonQuery):
    pass


def report_probe_collectors(*, field_key=None, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = ProbeCollectorQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/pc%s' % (field_key, query()))
    return handle_response(response_dict, 'rpc')


def report_probe_collectors_of_probe(*, field_key=None, probe_key, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = ProbeCollectorQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/s/%s/pc%s' % (field_key, probe_key, query()))
    return handle_response(response_dict, 'rpc')


def report_probe_collector(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_probe_collectors(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class ProbeCollectorUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 acoustic_a=None,
                 squelch_threshold=None,
                 lobe_range=None,
                 lobe_range_poles=None,
                 lobe_bearing_poles=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.acoustic_a = check_real_arg(acoustic_a)
        self.squelch_threshold = check_real_arg(squelch_threshold)
        self.lobe_range = check_real_arg(lobe_range)
        self.lobe_range_poles = check_string_arg(lobe_range_poles)
        self.lobe_bearing_poles = check_string_arg(lobe_bearing_poles)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.acoustic_a:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['aa'] = self.acoustic_a
        if self.squelch_threshold:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['st'] = self.squelch_threshold
        if self.lobe_range:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['lr'] = self.lobe_range
        if self.lobe_range_poles:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['lrp'] = self.lobe_range_poles
        if self.lobe_bearing_poles:
            if 'a' not in request_dict:
                request_dict['a'] = {}
            request_dict['a']['lbp'] = self.lobe_bearing_poles
        return request_dict


def update_probe_collectors(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'upc', 'trp/f/%s/pc' % field_key)
    return handle_response(response_dict, None)


def update_probe_collector(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_probe_collectors(field_key=field_key, updates=[ProbeCollectorUpdate(**kwargs)])


#
# Emitter Patch:
#

# Report:

class EmitterPatchQuery(CommonQuery):
    pass


def report_emitter_patches(*, field_key=None, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = EmitterPatchQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/smpe%s' % (field_key, query()))
    return handle_response(response_dict, 'rsmpe')


def report_emitter_patch(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_emitter_patches(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


def report_patch_of_field_emitter(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    query = CommonSectionsOnlyQuery(sections)
    response_dict = Sender.get('trp/f/%s/fe/%s/smpe%s' % (field_key, key, query()))
    return handle_response(response_dict, 'rsmpe')[0]


def report_patch_of_subject_emitter(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    query = CommonSectionsOnlyQuery(sections)
    response_dict = Sender.get('trp/f/%s/se/%s/smpe%s' % (field_key, key, query()))
    return handle_response(response_dict, 'rsmpe')[0]


def report_patch_of_probe_emitter(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    query = CommonSectionsOnlyQuery(sections)
    response_dict = Sender.get('trp/f/%s/pe/%s/smpe%s' % (field_key, key, query()))
    return handle_response(response_dict, 'rsmpe')[0]


# Update:

class EmitterPatchUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 patch_def=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.patch_def = check_patch_def_arg(patch_def)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.patch_def:
            request_dict['a'] = {}
            request_dict['a']['dpe'] = self.patch_def
        return request_dict


def update_emitter_patches(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'usmpe', 'trp/f/%s/smpe' % field_key)
    return handle_response(response_dict, None)


def update_emitter_patch(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_emitter_patches(field_key=field_key, updates=[EmitterPatchUpdate(**kwargs)])


#
# Oscillator Patch:
#

# Report:

class OscillatorPatchQuery(CommonQuery):
    pass


def report_oscillator_patches(*, field_key=None, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = OscillatorPatchQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/smpo%s' % (field_key, query()))
    return handle_response(response_dict, 'rsmpo')


def report_oscillator_patch(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_oscillator_patches(field_key=field_key, keys=[key], sections=sections)
    return None if not result else result[0]


def report_patch_of_field_oscillator(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    query = CommonSectionsOnlyQuery(sections)
    response_dict = Sender.get('trp/f/%s/fe/%s/smpo%s' % (field_key, key, query()))
    return handle_response(response_dict, 'rsmpo')[0]


def report_patch_of_subject_oscillator(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    query = CommonSectionsOnlyQuery(sections)
    response_dict = Sender.get('trp/f/%s/se/%s/smpo%s' % (field_key, key, query()))
    return handle_response(response_dict, 'rsmpo')[0]


def report_patch_of_probe_oscillator(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    query = CommonSectionsOnlyQuery(sections)
    response_dict = Sender.get('trp/f/%s/pe/%s/smpo%s' % (field_key, key, query()))
    return handle_response(response_dict, 'rsmpo')[0]


# Update:

class OscillatorPatchUpdate:
    def __init__(self,
                 key,
                 name=None,
                 description=None,
                 patch_def=None):
        self.key = check_key_arg(key)
        self.name = check_string_arg(name)
        self.description = check_string_arg(description)
        self.patch_def = check_patch_def_arg(patch_def)

    def __call__(self):
        request_dict = {
            'm': {
                'k': self.key}}
        if self.name:
            request_dict['m']['n'] = self.name
        if self.description:
            request_dict['m']['d'] = self.description
        if self.patch_def:
            request_dict['a'] = {}
            request_dict['a']['dpo'] = self.patch_def
        return request_dict


def update_oscillator_patches(*, field_key=None, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'usmpo', 'trp/f/%s/smpo' % field_key)
    return handle_response(response_dict, None)


def update_oscillator_patch(*, field_key=None, **kwargs):
    if not field_key:
        field_key = fk()
    return update_oscillator_patches(field_key=field_key, updates=[OscillatorPatchUpdate(**kwargs)])


#
# Oscillator Patch Envelope:
#

# Report:

class OscillatorPatchEnvelopeQuery(CommonQuery):
    pass


def report_oscillator_patch_envelopes(*, field_key=None, patch_key=None, keys=None, sections=None):
    if not field_key:
        field_key = fk()
    query = OscillatorPatchEnvelopeQuery(keys, sections)
    response_dict = Sender.get('trp/f/%s/smpo/%s/e%s' % (field_key, patch_key, query()))
    return handle_response(response_dict, 'resmpo')


def report_oscillator_patch_envelope(*, field_key=None, patch_key, key, sections=None):
    if not field_key:
        field_key = fk()
    result = report_oscillator_patch_envelopes(field_key=field_key, patch_key=patch_key, keys=[key], sections=sections)
    return None if not result else result[0]


# Update:

class OscillatorPatchEnvelopeUpdate:
    def __init__(self,
                 key,
                 envelope_def):
        self.key = check_string_arg(key)
        self.envelope_def = check_envelope_def_arg(envelope_def)

    def __call__(self):
        request_dict = {
            'k': self.key,
            'de': self.envelope_def}
        return request_dict


def update_oscillator_patch_envelopes(*, field_key=None, patch_key, updates):
    if not field_key:
        field_key = fk()
    response_dict = Sender.put(updates, 'usmpoe', 'trp/f/%s/smpo/%s/e' % (field_key, patch_key))
    return handle_response(response_dict, None)


def update_oscillator_patch_envelope(*, field_key=None, patch_key, **kwargs):
    if not field_key:
        field_key = fk()
    return update_oscillator_patch_envelopes(field_key=field_key,
                                             patch_key=patch_key,
                                             updates=[OscillatorPatchEnvelopeUpdate(**kwargs)])


#
# Waveforms
#

# Report:

class SamplerQuery:
    def __init__(self,
                 field_geometry=None,
                 antipode_distance=None,
                 collector_position=None,
                 collector_rotation=None,
                 acoustic_a=None,
                 squelch_threshold=None,
                 lobe_range=None,
                 lobe_range_poles=None,
                 lobe_bearing_poles=None,
                 sections=None):
        self.field_geometry = check_string_arg(field_geometry)
        self.antipode_distance = check_real_arg(antipode_distance)
        self.collector_position = self.convert_position(check_position_arg(collector_position))
        self.collector_rotation = check_rotation_arg(collector_rotation)
        self.acoustic_a = check_real_arg(acoustic_a)
        self.squelch_threshold = check_real_arg(squelch_threshold)
        self.lobe_range = check_real_arg(lobe_range)
        self.lobe_range_poles = check_string_arg(lobe_range_poles)
        self.lobe_bearing_poles = check_string_arg(lobe_bearing_poles)
        self.sections = check_string_arg(sections)

    def __call__(self):
        query = '?'
        if self.field_geometry:
            query += '&fg=%s' % self.field_geometry
        if self.antipode_distance:
            query += '&ad=%s' % self.antipode_distance
        if self.collector_position:
            query += '&cp=%s' % self.collector_position
        if self.collector_rotation:
            query += '&cr=%s' % self.collector_rotation
        if self.acoustic_a:
            query += '&aa=%s' % self.acoustic_a
        if self.squelch_threshold:
            query += '&st=%s' % self.squelch_threshold
        if self.lobe_range:
            query += '&lr=%s' % self.lobe_range
        if self.lobe_range_poles:
            query += '&lrp=%s' % self.lobe_range_poles
        if self.lobe_bearing_poles:
            query += '&lbp=%s' % self.lobe_bearing_poles
        if self.sections:
            query += ('&s=' + self.sections)
        return query if len(query) > 1 else ''

    @staticmethod
    def convert_position(position):
        return '%s~%s' % (position[0], position[1]) if position else None


def report_waveforms(*,
                     field_key=None,
                     field_geometry=None,
                     antipode_distance=None,
                     position=None,
                     rotation=None,
                     acoustic_a=None,
                     squelch_threshold=None,
                     lobe_range=None,
                     lobe_range_poles=None,
                     lobe_bearing_poles=None,
                     sections=None):
    if not field_key:
        field_key = fk()
    query = SamplerQuery(field_geometry=field_geometry,
                         antipode_distance=antipode_distance,
                         collector_position=position,
                         collector_rotation=rotation,
                         acoustic_a=acoustic_a,
                         squelch_threshold=squelch_threshold,
                         lobe_range=lobe_range,
                         lobe_range_poles=lobe_range_poles,
                         lobe_bearing_poles=lobe_bearing_poles,
                         sections=sections)
    response_dict = Sender.get('trp/f/%s/w%s' % (field_key, query()))
    return handle_response(response_dict, 'rw')


def report_waveforms_at_probe(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    query = CommonSectionsOnlyQuery(sections)
    response_dict = Sender.get('trp/f/%s/p/%s/w%s' % (field_key, key, query()))
    return handle_response(response_dict, 'rw')


def report_waveforms_at_probe_collector(*, field_key=None, key, sections=None):
    if not field_key:
        field_key = fk()
    query = CommonSectionsOnlyQuery(sections)
    response_dict = Sender.get('trp/f/%s/pc/%s/w%s' % (field_key, key, query()))
    return handle_response(response_dict, 'rw')


#
# Emitter Macros:
#

def create_channel(channel_tag, channel_envelope_def=None, oscillator_patch_def=None):
    args = [channel_tag]
    if channel_envelope_def:
        args += channel_envelope_def
    if oscillator_patch_def:
        args += oscillator_patch_def
    return {'create_channel': args}


def destroy_channel(channel_tag):
    return {'destroy_channel': [channel_tag]}


def set_channel_ceiling(channel_tag, ceiling):
    return {'set_channel_ceiling': [channel_tag, ceiling]}


def set_channel_poles(channel_tag, poles):
    return {'set_channel_poles': [channel_tag, poles]}


def set_channel_floor(channel_tag, floor):
    return {'set_channel_floor': [channel_tag, floor]}


#
# Oscillator Macros:
#

def set_loudness_ceiling(ceiling):
    return {'set_loudness_ceiling': [ceiling]}


def set_loudness_poles(poles):
    return {'set_loudness_poles': [poles]}


def set_loudness_floor(floor):
    return {'set_loudness_floor': [floor]}


def set_period_poles(poles):
    return {'set_period_poles': [poles]}


def set_pitch_ceiling(ceiling):
    return {'set_pitch_ceiling': [ceiling]}


def set_pitch_poles(poles):
    return {'set_pitch_poles': [poles]}


def set_pitch_floor(floor):
    return {'set_pitch_floor': [floor]}


def set_shape_poles(poles):
    return {'set_shape_poles': [poles]}


def set_tone_poles(poles):
    return {'set_tone_poles': [poles]}


def set_waveset_id(waveset_id):
    return {'set_waveset_id': [waveset_id]}
