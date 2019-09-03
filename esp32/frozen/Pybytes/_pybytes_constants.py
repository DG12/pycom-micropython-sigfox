'''
Copyright (c) 2019, Pycom Limited.
This software is licensed under the GNU GPL version 3 or any
later version, with permitted additional terms. For more information
see the Pycom Licence v1.0 document supplied with this file, or
available at https://www.pycom.io/opensource/licensing
'''

import sys


class MQTTConstants:
    # - Protocol types
    MQTTv3_1 = 3
    MQTTv3_1_1 = 4

    # - OfflinePublishQueueing drop behavior
    DROP_OLDEST = 0
    DROP_NEWEST = 1

    # Message types
    MSG_CONNECT = 0x10
    MSG_CONNACK = 0x20
    MSG_PUBLISH = 0x30
    MSG_PUBACK = 0x40
    MSG_PUBREC = 0x50
    MSG_PUBREL = 0x60
    MSG_PUBCOMP = 0x70
    MSG_SUBSCRIBE = 0x80
    MSG_SUBACK = 0x90
    MSG_UNSUBSCRIBE = 0xA0
    MSG_UNSUBACK = 0xB0
    MSG_PINGREQ = 0xC0
    MSG_PINGRESP = 0xD0
    MSG_DISCONNECT = 0xE0

    # Connection state
    STATE_CONNECTED = 0x01
    STATE_CONNECTING = 0x02
    STATE_DISCONNECTED = 0x03


class constants:
    __NETWORK_INFO_MASK = 0x30
    __NETWORK_TYPE_WIFI = 0
    __NETWORK_TYPE_LORA = 1
    __NETWORK_TYPE_SIGFOX = 2
    __NETWORK_TYPE_LTE = 3

    __INTEGER = 0
    __FLOAT = 1
    __TUPLE = 2
    __STRING = 3

    __CONNECTION_STATUS_DISCONNECTED = 0
    __CONNECTION_STATUS_CONNECTED_MQTT_WIFI = 1
    __CONNECTION_STATUS_CONNECTED_MQTT_LTE = 2
    __CONNECTION_STATUS_CONNECTED_LORA = 3
    __CONNECTION_STATUS_CONNECTED_SIGFOX = 4

    __PROTOCOL_VERSION = 0x04

    __TYPE_PING = 0x00
    __TYPE_INFO = 0x01
    __TYPE_NETWORK_INFO = 0x02
    __TYPE_SCAN_INFO = 0x03
    __TYPE_BATTERY_INFO = 0x04
    __TYPE_OTA = 0x05
    __TYPE_FCOTA = 0x06
    __TYPE_PONG = 0x07
    __TYPE_PYBYTES = 0x0E
    __PYBYTES_PROTOCOL = ">B%ds"
    __PYBYTES_PROTOCOL_PING = ">B"
    __PYBYTES_INTERNAL_PROTOCOL = ">BBH"
    __PYBYTES_INTERNAL_PROTOCOL_VARIABLE = ">BB%ds"

    __TERMINAL_PIN = 255

    __USER_SYSTEM = 1

    __COMMAND_PIN_MODE = 0
    __COMMAND_DIGITAL_READ = 1
    __COMMAND_DIGITAL_WRITE = 2
    __COMMAND_ANALOG_READ = 3
    __COMMAND_ANALOG_WRITE = 4
    __COMMAND_CUSTOM_METHOD = 5
    __COMMAND_CUSTOM_LOCATION = 6

    __FCOTA_COMMAND_HIERARCHY_ACQUISITION = 0x00
    __FCOTA_COMMAND_FILE_ACQUISITION = 0x01
    __FCOTA_COMMAND_FILE_UPDATE = 0x02
    __FCOTA_PING = 0x03
    __FCOTA_COMMAND_FILE_DELETE = 0x04

    __DEVICE_TYPE_WIPY = 0x00
    __DEVICE_TYPE_LOPY = 0x01
    __DEVICE_TYPE_WIPY_2 = 0x02
    __DEVICE_TYPE_SIPY = 0x03
    __DEVICE_TYPE_LOPY_4 = 0x04
    __DEVICE_TYPE_UNKNOWN = 0x05

    # {"ssid":"%s", "mac_addr":"%s", "channel":"%s", "power":"%s"}
    __WIFI_NETWORK_FORMAT = ">6sBb"

    # __USER_SYSTEM_MASK = 0x80
    __NETWORK_TYPE_MASK = 0x30
    __TYPE_MASK = 0xF

    __SIGFOX_WARNING = """WARNING! Your sigfox radio configuration (RC) is currently using the default (1)
You can set your RC with command (ex: RC 3): pybytes.set_config('sigfox', {'RCZ': 3})
See all available zone options for RC at https://support.sigfox.com/docs/radio-configuration """ # noqa
    __ONE_MINUTE = 60  # in seconds
    __KEEP_ALIVE_PING_INTERVAL = 600  # in seconds
    # set watch dog timeout to 21 minutes ~ (2 * 10) + 1
    __WDT_TIMEOUT_MILLISECONDS = (2 * __KEEP_ALIVE_PING_INTERVAL + __ONE_MINUTE) * 1000 # noqa

    __WDT_MAX_TIMEOUT_MILLISECONDS = sys.maxsize

    __DEFAULT_DOMAIN = 'pybytes.pycom.io'
    __DEFAULT_SW_HOST = 'software.pycom.io'