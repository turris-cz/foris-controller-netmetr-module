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

import json
import logging

from foris_controller.app import app_info
from foris_controller.utils import RWLock
from foris_controller_backends.cmdline import AsyncCommand
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
            sync_code = get_option_named(data, "netmetr", "settings", "sync_code", "")
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

    def update_settings(self, autostart_enabled, hours_to_run=None):

        with UciBackend() as backend:
            backend.set_option(
                "netmetr", "settings", "autostart_enabled", store_bool(autostart_enabled))
            if hours_to_run is not None:
                backend.replace_list("netmetr", "settings", "hours_to_run", hours_to_run)

        return True


class NetmetrDataFile(object):
    DATA_FILE_PATH = "/tmp/netmetr-history.json"
    data_file_lock = RWLock(app_info["lock_backend"])

    def read_records(self):
        with self.data_file_lock.readlock:
            try:
                with open(NetmetrDataFile.DATA_FILE_PATH) as f:
                    data = json.load(f)
            except IOError:
                return "missing", []
            except ValueError:
                return "error", []  # invalid json

        if len(data["error"]) > 0:
            return "error", []  # error indicator was set

        res = []
        for record in data["history"]:
            res.append({
                "speed_download": float(record["speed_download"]),
                "speed_upload": float(record["speed_upload"]),
                "ping": float(record["ping"]),
                "time": int(record["time"]) / 1000,  # -> to second precision
                "test_uuid": record["test_uuid"],
            })
        return "ready", res


class NetmetrCmds(AsyncCommand):
    def download_data(self, exit_notify, reset_notify):
        logger.debug("Starting to download netmetr data.")

        def handler_exit(process_data):
            exit_notify({"async_id": process_data.id, "passed": process_data.get_retval() == 0})
            logger.debug(
                "Downloading netmetr data finished: (retval=%d)" % process_data.get_retval())

        process_id = self.start_process(
            ["/usr/bin/netmetr", "--dwlhist", "--no-color", "--no-run"],
            [],  # no notifications only the exit one
            handler_exit,
            reset_notify,
        )
        logger.debug("Dowloading netmetr data started '%s'." % process_id)
        return process_id

    def measure_and_download_data(self, notify, exit_notify, reset_notify):
        logger.debug("Starting to measure and download netmetr data.")

        def handler_text_gen(regex, percent, msg):
            def handler(matched, process_data):
                notify({"async_id": process_data.id, "percent": percent, "msg": msg})

            return regex, handler

        def handler_ping(matched, process_data):
            attempt, value = matched.groups()
            notify({
                "async_id": process_data.id, "percent": 10 + int(attempt) * 5,
                "msg": "ping %sms" % value
            })

        def handler_sync_code(matched, process_data):
            sync_code = matched.groups()
            notify(
                {"async_id": process_data.id, "percent": 100, "msg": "sync_code %s" % sync_code})

        def handler_exit(process_data):
            exit_notify({"async_id": process_data.id, "passed": process_data.get_retval() == 0})
            logger.debug(
                "Measuring and downloading netmetr data finished: (retval=%d)"
                % process_data.get_retval()
            )

        process_id = self.start_process(
            ["/usr/bin/netmetr", "--dwlhist", "--no-color"],
            [
                handler_text_gen(r"^Starting ping test...$", 5, "ping start"),
                (r"^ping_([0-9]+)_msec = ([0-9]+.?[0-9]?)", handler_ping),
                handler_text_gen(r"^Starting speed test...$", 65, "speed start"),
                handler_text_gen(r"^pretest downlink start...", 70, "speed downlink start"),
                handler_text_gen(r"^downlink test end.$", 80, "speed downlink end"),
                handler_text_gen(r"^pretest uplink start...", 85, "speed uplink start"),
                handler_text_gen(r"^uplink test end.$", 90, "speed uplink end"),
                (r"^Your Sync code is:\s*([0-9a-zA-Z]+)", handler_sync_code),
            ],
            handler_exit,
            reset_notify,
        )

        logger.debug("Measuring and dowloading netmetr data started '%s'." % process_id)
        return process_id
