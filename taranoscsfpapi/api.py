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

#
# This package implements the Taranos "Pseudo-API".  It is intended to be a functional reference for Taranos web API
# familiarization.  It may also serve as the basis for other utilitarian purposes, however the user is advised that
# its network interfacing code is naive and would require significant enhancement to be considered "production-ready".
#

from taranoscsfpapi.sender import *


class ErrorCodes:
    Ok = 0
    KeyInvalid = -10
    KeysInvalid = -11
    SignalInvalid = -20
    SignalModeIndeterminate = -21
    PositionInvalid = -50
    RotationInvalid = -51
    ChannelDefinitionInvalid = -60
    EnvelopeDefinitionInvalid = -61
    PoleDefinitionInvalid = -62
    MacroUnsupported = -70
    MacroInvalid = -71
    FieldKeyInvalid = -100
    FieldUnknown = -101
    FieldInvalid = -102
    FieldUnavailable = -103
    FieldConstructorInvalid = -104
    FieldDestructorInvalid = -105
    FieldUpdateInvalid = -106
    FieldEmitterKeyInvalid = -110
    FieldEmitterUnknown = -111
    FieldEmitterInvalid = -112
    FieldEmitterUnavailable = -113
    FieldEmitterConstructorInvalid = -114
    FieldEmitterDestructorInvalid = -115
    FieldEmitterUpdateInvalid = -116
    FieldEmitterCallInvalid = -117
    FieldEmitterPatchless = -118
    FieldOscillatorKeyInvalid = -120
    FieldOscillatorUnknown = -121
    FieldOscillatorInvalid = -122
    FieldOscillatorUnavailable = -123
    FieldOscillatorConstructorInvalid = -124
    FieldOscillatorDestructorInvalid = -125
    FieldOscillatorUpdateInvalid = -126
    FieldOscillatorCallInvalid = -127
    FieldOscillatorPatchless = -128
    SubjectKeyInvalid = -130
    SubjectUnknown = -131
    SubjectInvalid = -132
    SubjectUnavailable = -133
    SubjectConstructorInvalid = -134
    SubjectDestructorInvalid = -135
    SubjectUpdateInvalid = -136
    SubjectEmitterKeyInvalid = -140
    SubjectEmitterUnknown = -141
    SubjectEmitterInvalid = -142
    SubjectEmitterUnavailable = -143
    SubjectEmitterConstructorInvalid = -144
    SubjectEmitterDestructorInvalid = -145
    SubjectEmitterUpdateInvalid = -146
    SubjectEmitterCallInvalid = -147
    SubjectEmitterPatchless = -148
    SubjectOscillatorKeyInvalid = -150
    SubjectOscillatorUnknown = -151
    SubjectOscillatorInvalid = -152
    SubjectOscillatorUnavailable = -153
    SubjectOscillatorConstructorInvalid = -154
    SubjectOscillatorDestructorInvalid = -155
    SubjectOscillatorUpdateInvalid = -156
    SubjectOscillatorCallInvalid = -157
    SubjectOscillatorPatchless = -158
    ProbeKeyInvalid = -160
    ProbeUnknown = -161
    ProbeInvalid = -162
    ProbeUnavailable = -163
    ProbeConstructorInvalid = -164
    ProbeDestructorInvalid = -165
    ProbeUpdateInvalid = -166
    ProbeEmitterKeyInvalid = -170
    ProbeEmitterUnknown = -171
    ProbeEmitterInvalid = -172
    ProbeEmitterUnavailable = -173
    ProbeEmitterConstructorInvalid = -174
    ProbeEmitterDestructorInvalid = -175
    ProbeEmitterUpdateInvalid = -176
    ProbeEmitterCallInvalid = -177
    ProbeEmitterPatchless = -178
    ProbeOscillatorKeyInvalid = -180
    ProbeOscillatorUnknown = -181
    ProbeOscillatorInvalid = -182
    ProbeOscillatorUnavailable = -183
    ProbeOscillatorConstructorInvalid = -184
    ProbeOscillatorDestructorInvalid = -185
    ProbeOscillatorUpdateInvalid = -186
    ProbeOscillatorCallInvalid = -187
    ProbeOscillatorPatchless = -158
    ProbeCollectorKeyInvalid = -190
    ProbeCollectorUnknown = -191
    ProbeCollectorInvalid = -192
    ProbeCollectorUnavailable = -193
    ProbeCollectorConstructorInvalid = -194
    ProbeCollectorDestructorInvalid = -195
    ProbeCollectorUpdateInvalid = -196
    EmitterPatchKeyInvalid = -300
    EmitterPatchUnknown = -301
    EmitterPatchInvalid = -302
    EmitterPatchUnavailable = -303
    EmitterPatchConstructorInvalid = -304
    EmitterPatchDestructorInvalid = -305
    EmitterPatchUpdateInvalid = -306
    EmitterPatchTapless = -307
    OscillatorPatchKeyInvalid = -310
    OscillatorPatchUnknown = -311
    OscillatorPatchInvalid = -312
    OscillatorPatchUnavailable = -313
    OscillatorPatchConstructorInvalid = -314
    OscillatorPatchDestructorInvalid = -315
    OscillatorPatchUpdateInvalid = -316
    OscillatorPatchTapless = -317
    OscillatorPatchBroken = -318
    SignalInputKeyInvalid = -330
    SignalInputUnknown = -331
    SignalInputInvalid = -332
    SignalInputUnavailable = -333
    SignalInputConstructorInvalid = -334
    SignalInputDestructorInvalid = -335
    SignalInputUpdateInvalid = -336
    SignalInputTapless = -337
    SignalBridgeKeyInvalid = -340
    SignalBridgeUnknown = -341
    SignalBridgeInvalid = -342
    SignalBridgeUnavailable = -343
    SignalBridgeConstructorInvalid = -344
    SignalBridgeDestructorInvalid = -345
    SignalBridgeUpdateInvalid = -346
    SignalBridgeTapless = -347
    SignalOutputKeyInvalid = -350
    SignalOutputUnknown = -351
    SignalOutputInvalid = -352
    SignalOutputUnavailable = -353
    SignalOutputConstructorInvalid = -354
    SignalOutputDestructorInvalid = -355
    SignalOutputUpdateInvalid = -356
    SignalOutputTapless = -357
    SignalOutputBroken = -358
    TrunkKeyInvalid = -400
    TrunkUnknown = -401
    TrunkInvalid = -402
    TrunkUnavailable = -403
    TrunkConstructorInvalid = -404
    TrunkDestructorInvalid = -405
    TrunkUpdateInvalid = -406
    SignalInterfaceKeyInvalid = -410
    SignalInterfaceUnknown = -411
    SignalInterfaceInvalid = -412
    SignalInterfaceUnavailable = -413
    SignalInterfaceConstructorInvalid = -414
    SignalInterfaceDestructorInvalid = -415
    SignalInterfaceUpdateInvalid = -416
    SignalPortKeyInvalid = -420
    SignalPortUnknown = -421
    SignalPortInvalid = -422
    SignalPortUnavailable = -423
    SignalPortConstructorInvalid = -424
    SignalPortDestructorInvalid = -425
    SignalPortUpdateInvalid = -426
    SignalPortTapless = -427
    SignalSourceKeyInvalid = -430
    SignalSourceUnknown = -431
    SignalSourceInvalid = -432
    SignalSourceUnavailable = -433
    SignalSourceConstructorInvalid = -434
    SignalSourceDestructorInvalid = -435
    SignalSourceUpdateInvalid = -436
    SignalSourceLinkless = -437
    SignalSinkKeyInvalid = -440
    SignalSinkUnknown = -441
    SignalSinkInvalid = -442
    SignalSinkUnavailable = -443
    SignalSinkConstructorInvalid = -444
    SignalSinkDestructorInvalid = -445
    SignalSinkUpdateInvalid = -446
    SignalSinkTapless = -447
    SignalLinkKeyInvalid = -450
    SignalLinkUnknown = -451
    SignalLinkInvalid = -452
    SignalLinkUnavailable = -453
    SignalLinkConstructorInvalid = -454
    SignalLinkDestructorInvalid = -455
    SignalLinkUpdateInvalid = -456
    SignalLinkSinkless = -457
    SignalTapKeyInvalid = -460
    SignalTapUnknown = -461
    SignalTapInvalid = -462
    SignalTapUnavailable = -463
    SignalTapConstructorInvalid = -464
    SignalTapDestructorInvalid = -465
    SignalTapUpdateInvalid = -466
    SignalTapSourceless = -467
    SignalTapSinkless = -468
    SignalTapModulatorless = -469


class PapiException (Exception):
    def __init__(self, code, text):
        self.args = (code, text)
        self.errno = code
        self.errmsg = text
        
        
class CommonQuery:
    def __init__(self,
                 keys,
                 sections=None):
        self.keys = check_list_arg(keys)
        self.sections = check_string_arg(sections)

    def __call__(self):
        query = ''
        if self.keys:
            query += '?'
            for key in self.keys:
                query += 'k=%s' % key
                if key != self.keys[-1]:
                    query += '&'
        if self.sections:
            query += ('%ss=' % ('&' if self.keys else '?') + self.sections)
        return query


class CommonSectionsOnlyQuery:
    def __init__(self,
                 sections=None):
        self.sections = check_string_arg(sections)

    def __call__(self):
        query = ''
        if self.sections:
            query += ('?s=' + self.sections)
        return query


def check_integer_arg(value):
    if value:
        if not isinstance(value, int):
            raise PapiException(-1, 'int arg invalid')
        return str(value)
    else:
        return None


def check_key_arg(value):
    if value:
        if not isinstance(value, str) or '~' not in value:
            raise PapiException(-1, 'string arg invalid')
        return value
    else:
        return None


def check_list_arg(value):
    if value and type(value) is not list:
        raise PapiException(-1, 'list arg invalid')
    return value


def check_real_arg(value):
    if value:
        if not isinstance(value, float):
            raise PapiException(-1, 'real arg invalid')
        return str(value)
    else:
        return None


def check_string_arg(value):
    if value:
        if not isinstance(value, str):
            raise PapiException(-1, 'string arg invalid')
        return value
    else:
        return None


def handle_response(response_dict, reply_key):
    """
    Process a response from the Taranos Server.

    :param response_dict: Response dict from the server
    :param reply_key: Expected reply key
    :return: Contents of the response dict indexed by the specified reply key
    :raise PapiException:
    """
    if not response_dict:
        raise PapiException(-1, 'invalid response received')
    status_code = response_dict['s']
    if status_code == 0:
        result_code = response_dict['r']
        if result_code == 0:
            if reply_key is None:
                return None
            else:
                return response_dict[reply_key]
        else:
            raise PapiException(result_code, response_dict['e'])


class Globals:
    fk = None   # Default field key.
    tk = None   # Default trunk key.

Globals = Globals()


def papi_init(server_url=None, is_verbose=False):
    """
    Initialize the Pseudo-API.

    :param server_url: URL of the Taranos Server
    """
    global Globals

    SingleSender(server_url, is_verbose)

    try:
        response_dict = Sender.get('tmp/c')
        cell_report = handle_response(response_dict, 'rc')
        Globals.fk = cell_report['mf']['_f']
        Globals.tk = cell_report['mt']['_t']

    except PapiException as e:
        print('taranoscsfpapi init failed (%s)' % e.__repr__)
