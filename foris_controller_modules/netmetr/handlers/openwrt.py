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

from foris_controller.handler_base import BaseOpenwrtHandler
from foris_controller.utils import logger_wrapper

from foris_controller_backends.netmetr import NetmetrUci, NetmetrDataFile, NetmetrCmds

from .. import Handler

logger = logging.getLogger(__name__)


class OpenwrtNetmetrHandler(Handler, BaseOpenwrtHandler):
    uci = NetmetrUci()
    data = NetmetrDataFile()
    cmds = NetmetrCmds()

    @logger_wrapper(logger)
    def get_settings(self):
        return self.uci.get_settings()

    @logger_wrapper(logger)
    def update_settings(self, autostart_enabled, hours_to_run=None):
        return self.uci.update_settings(autostart_enabled, hours_to_run)

    @logger_wrapper(logger)
    def get_data(self):
        status, data = self.data.read_records()
        return {"status": status, "performed_tests": data}

    @logger_wrapper(logger)
    def download_data_trigger(self, exit_notify, reset_notify):
        return OpenwrtNetmetrHandler.cmds.download_data(exit_notify, reset_notify)

    @logger_wrapper(logger)
    def measure_and_download_data_trigger(self, notify, exit_notify, reset_notify):
        return OpenwrtNetmetrHandler.cmds.measure_and_download_data(
            notify, exit_notify, reset_notify)
