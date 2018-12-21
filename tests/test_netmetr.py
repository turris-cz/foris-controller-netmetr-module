#
# foris-controller-netmetr-module
# Copyright (C) 2017 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#

import pytest
import textwrap

from foris_controller_testtools.fixtures import (
    backend, infrastructure, ubusd_test, uci_configs_init, FILE_ROOT_PATH,
    mosquitto_test, start_buses
)

from foris_controller_testtools.utils import FileFaker


@pytest.fixture(scope="function")
def netmetr_data(request):
    content = """\
        {
          "error": [],
          "history": [
            {
              "speed_download": "920",
              "speed_upload": "910",
              "ping_shortest_classification": 3,
              "test_type_id": 1,
              "speed_download_classification": 3,
              "ping": "0.78",
              "ping_shortest": "0.78",
              "time_string": "Aug 17, 2018 2:17:00 AM",
              "speed_upload_classification": 3,
              "time": 1534472220000,
              "ping_classification": 3,
              "timezone": "CEST",
              "model": "Turris",
              "test_uuid": "28a371fc-e310-48b5-9804-fe12cbfb692a",
              "network_type": "LAN"
            },
            {
              "speed_download": "880",
              "speed_upload": "890",
              "ping_shortest_classification": 3,
              "test_type_id": 1,
              "speed_download_classification": 3,
              "ping": "0.76",
              "ping_shortest": "0.76",
              "time_string": "Aug 16, 2018 2:28:31 AM",
              "speed_upload_classification": 3,
              "time": 1534386511000,
              "ping_classification": 3,
              "timezone": "CEST",
              "model": "Turris",
              "test_uuid": "a2148440-89a6-4ef3-a184-8f2009fc2939",
              "network_type": "LAN"
            },
            {
              "speed_download": "910",
              "speed_upload": "910",
              "ping_shortest_classification": 3,
              "test_type_id": 1,
              "speed_download_classification": 3,
              "ping": "0.71",
              "ping_shortest": "0.71",
              "time_string": "Aug 15, 2018 2:27:46 AM",
              "speed_upload_classification": 3,
              "time": 1534300066000,
              "ping_classification": 3,
              "timezone": "CEST",
              "model": "Turris",
              "test_uuid": "7f004e22-cd8a-470b-a1b0-9139c68632c9",
              "network_type": "LAN"
            },
            {
              "speed_download": "930",
              "speed_upload": "920",
              "ping_shortest_classification": 3,
              "test_type_id": 1,
              "speed_download_classification": 3,
              "ping": "0.77",
              "ping_shortest": "0.77",
              "time_string": "Aug 14, 2018 2:26:43 AM",
              "speed_upload_classification": 3,
              "time": 1534213603000,
              "ping_classification": 3,
              "timezone": "CEST",
              "model": "Turris",
              "test_uuid": "19a7ecc9-034d-40da-93a3-f002e8843057",
              "network_type": "LAN"
            },
            {
              "speed_download": "920",
              "speed_upload": "920",
              "ping_shortest_classification": 3,
              "test_type_id": 1,
              "speed_download_classification": 3,
              "ping": "0.71",
              "ping_shortest": "0.71",
              "time_string": "Aug 13, 2018 1:45:24 PM",
              "speed_upload_classification": 3,
              "time": 1534167924000,
              "ping_classification": 3,
              "timezone": "CEST",
              "model": "Turris",
              "test_uuid": "66ef8238-2bf6-4a2c-8a22-99b14c01b6cb",
              "network_type": "LAN"
            },
            {
              "speed_download": "920",
              "speed_upload": "930",
              "ping_shortest_classification": 3,
              "test_type_id": 1,
              "speed_download_classification": 3,
              "ping": "0.79",
              "ping_shortest": "0.79",
              "time_string": "Aug 13, 2018 4:50:01 AM",
              "speed_upload_classification": 3,
              "time": 1534135801000,
              "ping_classification": 3,
              "timezone": "CEST",
              "model": "Turris",
              "test_uuid": "a498c3a9-c077-4d3b-bb42-aa0f760558df",
              "network_type": "LAN"
            },
            {
              "speed_download": "910",
              "speed_upload": "910",
              "ping_shortest_classification": 3,
              "test_type_id": 1,
              "speed_download_classification": 3,
              "ping": "0.74",
              "ping_shortest": "0.74",
              "time_string": "Aug 13, 2018 2:24:07 AM",
              "speed_upload_classification": 3,
              "time": 1534127047000,
              "ping_classification": 3,
              "timezone": "CEST",
              "model": "Turris",
              "test_uuid": "f93d5d91-dc47-4b64-a957-26cb24f3251a",
              "network_type": "LAN"
            },
            {
              "speed_download": "880",
              "speed_upload": "900",
              "ping_shortest_classification": 3,
              "test_type_id": 1,
              "speed_download_classification": 3,
              "ping": "0.74",
              "ping_shortest": "0.74",
              "time_string": "Aug 12, 2018 2:18:12 AM",
              "speed_upload_classification": 3,
              "time": 1534040292000,
              "ping_classification": 3,
              "timezone": "CEST",
              "model": "Turris",
              "test_uuid": "c7589adb-1f44-4710-8511-4d0cc6c96a6b",
              "network_type": "LAN"
            },
            {
              "speed_download": "800",
              "speed_upload": "770",
              "ping_shortest_classification": 3,
              "test_type_id": 1,
              "speed_download_classification": 3,
              "ping": "0.73",
              "ping_shortest": "0.73",
              "time_string": "Aug 11, 2018 2:25:38 AM",
              "speed_upload_classification": 3,
              "time": 1533954338000,
              "ping_classification": 3,
              "timezone": "CEST",
              "model": "Turris",
              "test_uuid": "73f2469d-0e09-4d56-8536-7bfe9af9f9b6",
              "network_type": "LAN"
            },
            {
              "speed_download": "920",
              "speed_upload": "890",
              "ping_shortest_classification": 3,
              "test_type_id": 1,
              "speed_download_classification": 3,
              "ping": "0.64",
              "ping_shortest": "0.64",
              "time_string": "Aug 10, 2018 2:11:35 AM",
              "speed_upload_classification": 3,
              "time": 1533867095000,
              "ping_classification": 3,
              "timezone": "CEST",
              "model": "Turris",
              "test_uuid": "586bd913-abd0-433b-bef4-745b3c4ad034",
              "network_type": "LAN"
            }
          ]
        }"""
    with FileFaker(
        FILE_ROOT_PATH, "/tmp/netmetr-history.json",
        False, textwrap.dedent(content)
    ) as f:
        yield f, content


def test_settings(uci_configs_init, infrastructure, start_buses):
    notifications = infrastructure.get_notifications()

    res = infrastructure.process_message({
        "module": "netmetr",
        "action": "get_settings",
        "kind": "request",
    })
    assert set(res["data"].keys()) == {"autostart_enabled", "hours_to_run", "sync_code"}
    sync_code = res["data"]["sync_code"]
    new_autostart_enabled = not res["data"]["autostart_enabled"]
    new_hours_to_run = [e for e in range(24) if e not in res["data"]["hours_to_run"]]

    res = infrastructure.process_message({
        "module": "netmetr",
        "action": "update_settings",
        "kind": "request",
        "data": {
            "autostart_enabled": new_autostart_enabled,
            "hours_to_run": new_hours_to_run,
        }
    })
    assert res["data"] == {"result": True}

    notifications = infrastructure.get_notifications(notifications)
    assert notifications[-1] == {
        u"module": u"netmetr",
        u"action": u"update_settings",
        u"kind": u"notification",
        u"data": {u"autostart_enabled": new_autostart_enabled, u"hours_to_run": new_hours_to_run},
    }

    res = infrastructure.process_message({
        "module": "netmetr",
        "action": "get_settings",
        "kind": "request",
    })
    assert res == {
        u"module": u"netmetr",
        u"action": u"get_settings",
        u"kind": u"reply",
        u"data": {
            u"sync_code": sync_code,
            u"autostart_enabled": new_autostart_enabled,
            u"hours_to_run": new_hours_to_run
        },
    }

    # command without hours_to_run
    new_autostart_enabled = not new_autostart_enabled
    res = infrastructure.process_message({
        "module": "netmetr",
        "action": "update_settings",
        "kind": "request",
        "data": {
            "autostart_enabled": new_autostart_enabled,
        }
    })
    assert res["data"] == {"result": True}

    notifications = infrastructure.get_notifications(notifications)
    assert notifications[-1] == {
        u"module": u"netmetr",
        u"action": u"update_settings",
        u"kind": u"notification",
        u"data": {u"autostart_enabled": new_autostart_enabled},
    }

    res = infrastructure.process_message({
        "module": "netmetr",
        "action": "get_settings",
        "kind": "request",
    })
    assert res == {
        u"module": u"netmetr",
        u"action": u"get_settings",
        u"kind": u"reply",
        u"data": {
            u"sync_code": sync_code,
            u"autostart_enabled": new_autostart_enabled,
            u"hours_to_run": new_hours_to_run
        },
    }


def test_get_data(uci_configs_init, infrastructure, start_buses, netmetr_data):
    res = infrastructure.process_message({
        "module": "netmetr",
        "action": "get_data",
        "kind": "request",
    })
    assert set(res["data"].keys()) == {"status", "performed_tests"}


def test_download_data(uci_configs_init, infrastructure, start_buses):
    res = infrastructure.process_message({
        "module": "netmetr",
        "action": "download_data",
        "kind": "request",
    })
    assert set(res["data"].keys()) == {"async_id"}


def test_measure_and_download_data(uci_configs_init, infrastructure, start_buses):
    res = infrastructure.process_message({
        "module": "netmetr",
        "action": "measure_and_download_data",
        "kind": "request",
    })
    assert set(res["data"].keys()) == {"async_id"}
