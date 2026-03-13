"""
UPDI NVM implementation - extended
"""
from typing import Any

import logging

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
    NVM Access the UPDI way
    """
    #pylint: disable=non-parent-init-called, super-init-not-called
    #we want to set up the debug session much later
    def __init__(self, transport :  HidTransportBase,
                    device_info :  dict[ str, Any ],
                    manage : list[str] | None = None):
        self.manage : list[str] = [] if manage is None else manage
        self.logger_local : logging.Logger = logging.getLogger('pyavrocd.nvmupdi')
        NvmAccessProviderCmsisDapAvr.__init__(self, device_info)
        self.options : dict[str, Any] = {}
        self.avr : AvrDevice = XTinyXAvrTarget(transport)

    # pylint: disable=arguments-differ
    # reason for the difference: PyAvrOCD passes a prog_mode flag through all NVM wrappers
    def read(self, memory_info : dict[ str, Any ], offset : int,
                 numbytes : int, prog_mode : bool=False) -> bytearray:
        """
        Read memory in chunks.
        """
        _dummy = prog_mode
        memtype_string : str = memory_info[DeviceMemoryInfoKeys.NAME]
        memtype : int = self.avr.memtype_read_from_string(memtype_string)
        if memtype == 0:
            msg : str = "Unsupported memory type: {}".format(memtype_string)
            self.logger_local.error(msg)
            raise PymcuprogError(msg)

        if memtype_string != MemoryNames.FLASH:
            try:
                offset += memory_info[DeviceMemoryInfoKeys.ADDRESS]
            except TypeError:
                pass

        self.logger_local.debug("Reading from %s at %X %d bytes",
                                memory_info['name'], offset, numbytes)
        return self.avr.read_memory_section(memtype, offset, numbytes, numbytes)

    def write(self, memory_info : dict[ str, Any ], offset : int,
                  data : bytes, prog_mode : bool=False) -> None:
        """
        Write memory with data.
        """
        _dummy = prog_mode
        if len(data) == 0:
            return
        data_in : bytearray = bytearray(data)
        memtype_string : str = memory_info[DeviceMemoryInfoKeys.NAME]
        memtype : int = self.avr.memtype_write_from_string(memtype_string)
        if memtype == 0:
            msg : str = "Unsupported memory type: {}".format(memtype_string)
            self.logger_local.error(msg)
            raise PymcuprogError(msg)

        data_to_write : bytes
        address : int
        if memtype_string != MemoryNames.EEPROM:
            data_to_write, address = utils.pagealign(data_in,
                                                     offset,
                                                     memory_info[DeviceMemoryInfoKeys.PAGE_SIZE],
                                                     memory_info[DeviceMemoryInfoKeys.WRITE_SIZE])
        else:
            data_to_write = data_in
            address = offset

        if memtype_string != MemoryNames.FLASH:
            address += memory_info[DeviceMemoryInfoKeys.ADDRESS]

        allow_blank_skip : bool = memtype_string == MemoryNames.FLASH
        if memtype_string in (MemoryNames.FLASH, MemoryNames.EEPROM,
                              MemoryNames.FUSES, MemoryNames.LOCKBITS):
            write_chunk_size : int = memory_info[DeviceMemoryInfoKeys.PAGE_SIZE]
            if memtype_string != MemoryNames.EEPROM:
                data_to_write = utils.pad_to_size(data_to_write, write_chunk_size, 0xFF)
        else:
            write_chunk_size = len(data_to_write)

        self.logger_local.debug("Writing %d bytes of data in chunks of %d bytes to %s...",
                         len(data_to_write),
                         write_chunk_size,
                         memory_info[DeviceMemoryInfoKeys.NAME])

        first_chunk_size : int = write_chunk_size - address % write_chunk_size
        self.avr.write_memory_section(memtype,
                                      address,
                                      data_to_write[:first_chunk_size],
                                      write_chunk_size,
                                      allow_blank_skip=allow_blank_skip)
        address += first_chunk_size
        if len(data_to_write) > first_chunk_size:
            self.avr.write_memory_section(memtype,
                                          address,
                                          data_to_write[first_chunk_size:],
                                          write_chunk_size,
                                          allow_blank_skip=allow_blank_skip)

    def erase_page(self, addr : int, prog_mode : bool) -> bool:
        """
        Erase one flash page.
        """
        if not prog_mode:
            self.avr.switch_to_progmode()
        self.erase({DeviceMemoryInfoKeys.NAME: MemoryNames.FLASH}, addr)
        if not prog_mode:
            self.avr.switch_to_debmode()
        return True

    def erase_chip(self, prog_mode : bool) -> bool:
        """
        Erase the entire chip.
        """
        if not prog_mode:
            self.avr.switch_to_progmode()
        self.erase()
        if not prog_mode:
            self.avr.switch_to_debmode()
        return True
