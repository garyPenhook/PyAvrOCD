"""
UPDI NVM implementation - extended
"""
#Implementation is only a stub:
#pylint: disable=unused-import
from typing import Any

import logging

from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError
from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.hidtransport.hidtransportbase import HidTransportBase

from pymcuprog.nvmupdi import NvmAccessProviderCmsisDapUpdi
from pymcuprog.nvm import NvmAccessProviderCmsisDapAvr
from pymcuprog.pymcuprog_errors import PymcuprogError
from pymcuprog.avr8target import AvrDevice

from pymcuprog.deviceinfo.deviceinfokeys import DeviceMemoryInfoKeys
from pymcuprog.deviceinfo.memorynames import MemoryNames

from pymcuprog import utils

from pyavrocd.xavr8target import XTinyXAvrTarget

class XNvmAccessProviderCmsisDapUpdi(NvmAccessProviderCmsisDapUpdi):
    """
    NVM Access the DW way
    """
    #pylint: disable=non-parent-init-called, super-init-not-called
    #we want to set up the debug session much later
    def __init__(self, transport :  HidTransportBase,
                    device_info :  dict[ str, Any ],
                    manage : list[str] | None = None):
        self.manage : list[str] = [] if manage is None else manage
        self.logger_local : logging.Logger = logging.getLogger('pyavrocd.nvmupdi')
        NvmAccessProviderCmsisDapAvr.__init__(self, device_info)
        self.avr : AvrDevice = XTinyXAvrTarget(transport)

