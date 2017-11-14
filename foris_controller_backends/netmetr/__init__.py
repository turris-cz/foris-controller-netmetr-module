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

import logging

from foris_controller_backends.uci import (
    UciBackend, UciTypeException, UciRecordNotFound, get_option_named,
    parse_bool, store_bool
)


logger = logging.getLogger(__name__)


class NetmetrUci():
    def get_settings(self):
        with UciBackend() as backend:
            data = backend.read("netmetr")
            autostart_enabled = parse_bool(
                get_option_named(data, "netmetr", "settings", "autostart_enabled")
            )
            sync_code = get_option_named(data, "netmetr", "settings", "sync_code")
            try:
                hours_to_run = map(
                    int,
                    get_option_named(data, "netmetr", "settings", "hours_to_run")
                )
            except ValueError:
                raise UciTypeException(
                    get_option_named(data, "netmetr", "settings", "hours_to_run"),
                    "[int, int, ...]",
                )
            except UciRecordNotFound:
                hours_to_run = []
        return {
            "autostart_enabled": autostart_enabled,
            "hours_to_run": hours_to_run,
            "sync_code": sync_code,
        }

    def update_settings(self, autostart_enabled, hours_to_run):

        with UciBackend() as backend:
            backend.set_option(
                "netmetr", "settings", "autostart_enabled", store_bool(autostart_enabled))
            backend.replace_list("netmetr", "settings", "hours_to_run", hours_to_run)

        return True
