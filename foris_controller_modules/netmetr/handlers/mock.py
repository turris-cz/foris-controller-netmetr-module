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
import random

from foris_controller.handler_base import BaseMockHandler
from foris_controller.utils import logger_wrapper

from .. import Handler

logger = logging.getLogger(__name__)


class MockNetmetrHandler(Handler, BaseMockHandler):
    autostart_enabled = True
    hours_to_run = range(0, 24, 2)
    sync_code = "1af827965d0d"

    @logger_wrapper(logger)
    def get_settings(self):
        return {
            "sync_code": self.sync_code,
            "autostart_enabled": self.autostart_enabled,
            "hours_to_run": self.hours_to_run,
        }

    @logger_wrapper(logger)
    def update_settings(self, autostart_enabled, hours_to_run=None):
        self.autostart_enabled = autostart_enabled
        if hours_to_run:
            self.hours_to_run = hours_to_run
        return True

    @logger_wrapper(logger)
    def get_data(self):
        return random.choice([
            {"status": "error", "performed_tests": []},
            {"status": "missing", "performed_tests": []},
            {"status": "ready", "performed_tests": [
                {
                    "speed_download": 23,
                    "speed_upload": 53,
                    "ping": 0.57,
                    "time": 1510669694,
                    "test_uuid": "563803cc-b43e-4b2e-bf9e-439b098fe35b"
                },
                {
                    "speed_download": 88,
                    "speed_upload": 66,
                    "ping": 0.81,
                    "time": 1510669699,
                    "test_uuid": "a975e00d-0bca-4871-8ce3-6e33c12311ef"
                }
            ]},
        ])

    @logger_wrapper(logger)
    def download_data_trigger(self, exit_notify, reset_notify):
        return "%032X" % random.randrange(2**32)

    @logger_wrapper(logger)
    def measure_and_download_data_trigger(self, notify, exit_notify, reset_notify):
        return "%032X" % random.randrange(2**32)
