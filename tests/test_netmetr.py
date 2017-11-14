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

from .fixtures import backend, infrastructure, ubusd_test


def test_settings(infrastructure, ubusd_test):
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
