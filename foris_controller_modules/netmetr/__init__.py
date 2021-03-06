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

from foris_controller.module_base import BaseModule
from foris_controller.handler_base import wrap_required_functions


class NetmetrModule(BaseModule):
    logger = logging.getLogger(__name__)

    def action_get_settings(self, data):
        res = {}
        res.update(self.handler.get_settings())
        return res

    def action_update_settings(self, data):
        res = self.handler.update_settings(**data)
        if res:
            self.notify("update_settings", data)
        return {"result": res}

    def action_get_data(self, data):
        res = {}
        res.update(self.handler.get_data())
        return res

    def action_download_data(self, data):
        def exit_notify(msg):
            self.notify("download_data_finished", msg)
        return {
            "async_id": self.handler.download_data_trigger(exit_notify, self.reset_notify)
        }

    def action_measure_and_download_data(self, data):
        def notify(msg):
            self.notify("measure_and_download_data_notification", msg)

        def exit_notify(msg):
            self.notify("measure_and_download_data_finished", msg)

        return {
            "async_id": self.handler.measure_and_download_data_trigger(
                notify, exit_notify, self.reset_notify)
        }


@wrap_required_functions([
    'get_settings',
    'update_settings',
    'get_data',
    'download_data_trigger',
    'measure_and_download_data_trigger',
])
class Handler(object):
    pass
