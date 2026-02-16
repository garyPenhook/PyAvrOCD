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
from pyedbglib.util import binary

from pymcuprog.nvmupdi import NvmAccessProviderCmsisDapUpdi
from pymcuprog.nvm import NvmAccessProviderCmsisDapAvr
from pymcuprog.pymcuprog_errors import PymcuprogError
from pymcuprog.avr8target import AvrDevice

from pymcuprog.deviceinfo.deviceinfo import DeviceMemoryInfo
from pymcuprog.deviceinfo.deviceinfokeys import DeviceMemoryInfoKeys, DeviceInfoKeysAvr
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

    def read(self, memory_info : dict[ str, Any ], offset : int,
                 numbytes : int, prog_mode : bool=False) -> bytearray:
        """
        Read the memory in chunks

        :param memory_info: dictionary for the memory as provided by the DeviceMemoryInfo class
        :param offset: relative offset in the memory type
        :param numbytes: number of bytes to read
        :param prog_mode: True iff in programming mode
        :return: array of bytes read

        The super class will handle it (we simply remove the prog_mode parameter)
        """
        _dummy = prog_mode
        return super().read(memory_info, offset, numbytes)


    def write(self, memory_info : dict[ str, Any ], offset : int,
                  data : bytes, prog_mode : bool=False) -> None:
        """
        Write the memory with data

        :param memory_info: dictionary for the memory as provided by the DeviceMemoryInfo class
        :param offset: relative offset within the memory type
        :param data: the data to program

        The super class will handle it
        """
        _dummy = prog_mode
        super().write(memory_info, offset, data)

    def erase_page(self, pageaddr : int, memory_info: dict[ str, Any ], prog_mode : bool) -> bool:
        """
        Erase one page
        """
        _dummy = prog_mode
        self.erase(memory_info, pageaddr)
        return True

    def erase_chip(self, prog_mode : bool) -> bool :
        """
        Erasing entire chip. Save EEPROM by, potentially, reprogramming EESAVE fuse.
        Lockbits will never be set when this function is called since this is handled
        in _manage_fuses.
        """
        eesave_fuse_byte = None
        eesave_mask = self.device_info.get('eesave_mask')
        eesave_base = self.device_info.get('eesave_base')
        self.logger_local.debug("Erase Page: Manage:=%s, Mask=0x%X, Base=0x%X", self.manage, eesave_mask, eesave_base)
        if not prog_mode:
            self.avr.switch_to_progmode()
        if eesave_base and eesave_mask and 'eesave' in self.manage:
            self.logger_local.debug("Trying to preserve EEPROM")
            eesave_fuse_byte = self.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES,
                                                        eesave_base, 1)
            if  eesave_fuse_byte[0] & eesave_mask: # needs to be temporarily programmed
                self.logger_local.debug("EESAVE will be temporarily programmed")
                self.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, eesave_base,
                                          bytearray([eesave_fuse_byte[0] & ~eesave_mask & 0xFF]))
                self.logger_local.debug("Programmed EESAVE fuse temporarily")
            else:
                eesave_fuse_byte = None
        else:
            self.logger_local.error("EESAVE fuse data unknown. EEPROM will be deleted")
        self.avr.erase(Avr8Protocol.ERASE_CHIP, 0)
        self.logger_local.info("Flash memory erased")
        if eesave_fuse_byte: # needs to be restored
            self.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, eesave_base, eesave_fuse_byte)
            self.logger_local.debug("EESAVE fuse restored")
        if not prog_mode:
            self.avr.switch_to_debmode()
        return True

    def read_device_id(self) -> bytearray:
        """
        Read the device info

        :returns: Device ID raw bytes (little endian)
        """
        device_memory_info = DeviceMemoryInfo(self.device_info)
        signatures_info = device_memory_info.memory_info_by_name(MemoryNames.SIGNATURES)
        signatures_address = signatures_info[DeviceMemoryInfoKeys.ADDRESS]
        sig = self.avr.memory_read(self.avr.memtype_read_from_string("raw"),
                                   signatures_address,
                                   3)
        device_id_read = binary.unpack_be24(sig)

        self.logger.info("Device ID: '%06X'", device_id_read)

        revision = self.avr.memory_read(self.avr.memtype_read_from_string("raw"),
                                        self.device_info.get(DeviceInfoKeysAvr.SYSCFG_BASE) + 1, 1)
        self.logger.debug("Device revision: 0x%02x", revision[0])
        self.logger.info("Device revision: '%x.%x'", revision[0] >> 4, revision[0] & 0x0F)

        # Return the raw signature bytes, but swap the endianness as target sends ID as Big endian
        return bytearray([sig[2], sig[1], sig[0]])
