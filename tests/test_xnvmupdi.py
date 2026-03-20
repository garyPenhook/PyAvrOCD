"""
The test suit for the XNvmAccessProviderCmsisDapUpdi class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import Mock, MagicMock, create_autospec
from unittest import TestCase

from pymcuprog.deviceinfo import deviceinfo
from pymcuprog.deviceinfo.deviceinfokeys import DeviceMemoryInfoKeys
from pymcuprog.deviceinfo.memorynames import MemoryNames

from pyedbglib.protocols.avr8protocol import Avr8Protocol

from pyavrocd.xnvmupdi import XNvmAccessProviderCmsisDapUpdi
from pyavrocd.xavr8target import XTinyXAvrTarget
from pyavrocd.deviceinfo.devices.atmega4809 import DEVICE_INFO

class TestXNvmAccessProviderCmsisDapUpdi(TestCase):

    def setUp(self):
        self.nvm = None
        self.device_info = None
        self.memory_info = None

    def set_up(self):
        self.nvm = XNvmAccessProviderCmsisDapUpdi(MagicMock(), DEVICE_INFO, manage=None)
        self.nvm.avr = create_autospec(XTinyXAvrTarget)
        self.device_info = deviceinfo.getdeviceinfo("pyavrocd.deviceinfo.devices." + "atmega4809")
        self.memory_info = deviceinfo.DeviceMemoryInfo(self.device_info)
        self.nvm.logger_local.info = Mock()

    def test_init(self):
        self.set_up()
        self.assertTrue(self.nvm.avr is not None)

    def test_read_flash_accepts_prog_mode(self):
        self.set_up()
        flash_info = self.memory_info.memory_info_by_name('flash')
        self.nvm.avr.memtype_read_from_string.return_value = Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        self.nvm.avr.read_memory_section.return_value = bytearray([0x12, 0x34])
        self.assertEqual(self.nvm.read(flash_info, 0x20, 2, prog_mode=True), bytearray([0x12, 0x34]))
        self.nvm.avr.read_memory_section.assert_called_once_with(Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE,
                                                                 0x20, 2, 2)

    def test_read_eeprom_adds_offset(self):
        self.set_up()
        eeprom_info = self.memory_info.memory_info_by_name('eeprom')
        self.nvm.avr.memtype_read_from_string.return_value = Avr8Protocol.AVR8_MEMTYPE_EEPROM
        self.nvm.avr.read_memory_section.return_value = bytearray([0x56])
        self.assertEqual(self.nvm.read(eeprom_info, 0x10, 1, prog_mode=False), bytearray([0x56]))
        self.nvm.avr.read_memory_section.assert_called_once_with(Avr8Protocol.AVR8_MEMTYPE_EEPROM,
                                                                 eeprom_info[DeviceMemoryInfoKeys.ADDRESS] + 0x10,
                                                                 1, 1)

    def test_write_flash_accepts_prog_mode(self):
        self.set_up()
        flash_info = self.memory_info.memory_info_by_name('flash')
        self.nvm.avr.memtype_write_from_string.return_value = Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE
        self.nvm.write(flash_info, 0x00, b'\xAA\xBB', prog_mode=True)
        args, kwargs = self.nvm.avr.write_memory_section.call_args
        self.assertEqual(args[0], Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE)
        self.assertEqual(args[1], 0)
        self.assertEqual(args[2][:2], b'\xAA\xBB')
        self.assertEqual(len(args[2]), flash_info[DeviceMemoryInfoKeys.PAGE_SIZE])
        self.assertEqual(args[3], flash_info[DeviceMemoryInfoKeys.PAGE_SIZE])
        self.assertTrue(kwargs['allow_blank_skip'])

    def test_erase_page_switches_modes_when_needed(self):
        self.set_up()
        flash_info = self.memory_info.memory_info_by_name('flash')
        self.nvm.erase = Mock()
        self.assertTrue(self.nvm.erase_page(0x80, flash_info, False))
        self.nvm.avr.switch_to_progmode.assert_called_once_with()
        self.nvm.avr.switch_to_debmode.assert_called_once_with()
        self.nvm.erase.assert_called_once_with(flash_info, 0x80)

    def test_erase_chip_uses_existing_mode(self):
        self.set_up()
        self.assertTrue(self.nvm.erase_chip(True))
        self.nvm.avr.switch_to_progmode.assert_not_called()
        self.nvm.avr.switch_to_debmode.assert_not_called()
        self.nvm.avr.erase.assert_called_once_with(Avr8Protocol.ERASE_CHIP, 0)
