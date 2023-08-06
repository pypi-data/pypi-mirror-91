from __future__ import print_function

import os

from halo_app.classes import AbsBaseClass
from halo_app.domain.command import HaloCommand
from halo_app.domain.event import AbsHaloEvent
from halo_app.const import LOC, OPType
from halo_app.app.context import HaloContext, InitCtxFactory
from halo_app.app.request import HaloEventRequest, HaloCommandRequest, AbsHaloRequest, HaloQueryRequest
from halo_app.view.query import AbsHaloQuery, HaloQuery


class SysUtil(AbsBaseClass):
    @staticmethod
    def get_stage():
        """

        :return:
        """
        if 'HALO_STAGE' in os.environ:
            return os.environ['HALO_STAGE']
        return LOC

    @staticmethod
    def create_command_request(halo_context: HaloContext, method_id: str, vars: dict,
                               security=None, roles=None) -> AbsHaloRequest:
        halo_command = HaloCommand(halo_context, method_id, vars)
        return HaloCommandRequest(halo_command, security, roles)

    @staticmethod
    def create_event_request(halo_event: AbsHaloEvent,
                               security=None, roles=None) -> AbsHaloRequest:
        return HaloEventRequest(halo_event, security, roles)

    @staticmethod
    def create_query_request(halo_query: HaloQuery,
                               security=None, roles=None) -> AbsHaloRequest:
        return HaloQueryRequest(halo_query, security, roles)