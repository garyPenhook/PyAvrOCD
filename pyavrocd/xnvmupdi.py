"""
UPDI NVM implementation - extended
"""
from typing import Any

import logging

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
        self.avr : AvrDevice = XTinyXAvrTarget(transport, device_info=device_info)
        self.logger_local.debug("manage=%s", self.manage)

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

    def erase_page(self, pageaddr : int, memory_info : dict[ str, Any ], prog_mode : bool) -> bool:
        """
        Erase one flash page.
        """
        if not prog_mode:
            self.avr.switch_to_progmode()
        self.erase(memory_info, pageaddr)
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

    def erase_chip(self, prog_mode : bool) -> bool:
        """
        Erasing entire chip. Save EEPROM by, potentially, reprogramming EESAVE fuse.
        Lockbits will never be set when this function is called since this is handled
        in _manage_fuses.
        """
        eesave_fuse_byte = None
        eesave_mask = self.device_info.get('eesave_mask')
        eesave_base = self.device_info.get('eesave_base')
        self.logger_local.debug("Erase Chip: Manage:=%s, Mask=0x%X, Base=0x%X", self.manage,
                                    eesave_mask, eesave_base)
        if not prog_mode:
            self.avr.switch_to_progmode()
        eesave_fuse_byte = None
        if 'eesave' in self.manage:
            if eesave_base and eesave_mask:
                self.logger_local.debug("Trying to preserve EEPROM")
                eesave_fuse_byte = self.avr.memory_read(Avr8Protocol.AVR8_MEMTYPE_FUSES,
                                                        eesave_base, 1)
                if  eesave_fuse_byte[0] & eesave_mask: # needs to be temporarily programmed
                    self.logger_local.info("EESAVE will be temporarily programmed")
                    self.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, eesave_base,
                                            bytearray([eesave_fuse_byte[0] & ~eesave_mask & 0xFF]))
                    self.logger_local.debug("Programmed EESAVE fuse temporarily")
            else:
                self.logger_local.error("EESAVE fuse data unknown. EEPROM will be deleted")
        self.avr.erase(Avr8Protocol.ERASE_CHIP, 0)
        self.logger_local.info("Flash memory erased")
        if eesave_fuse_byte: # needs to be restored
            self.avr.memory_write(Avr8Protocol.AVR8_MEMTYPE_FUSES, eesave_base, eesave_fuse_byte)
            self.logger_local.info("EESAVE fuse restored")
        if not prog_mode:
            self.avr.switch_to_debmode()
        return True
