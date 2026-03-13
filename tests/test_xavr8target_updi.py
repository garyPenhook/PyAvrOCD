"""
The test suit for the XTinyAvrTarget class
"""
#pylint: disable=protected-access,missing-function-docstring,consider-using-f-string,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods
from unittest.mock import  MagicMock, create_autospec, call
from unittest import TestCase

from pyedbglib.protocols.avr8protocol import Avr8Protocol
from pyedbglib.util import binary

from pyavrocd.xavr8target import XTinyXAvrTarget
#from pyavrocd.deviceinfo.devices.atmega4809 import DEVICE_INFO


class TestXAvr8TargetUpdi(TestCase):

    def setUp(self):
        self.xa = None

    def set_up(self):
        self.xa = XTinyXAvrTarget(MagicMock())
        self.xa.protocol = create_autospec(Avr8Protocol)

    def test_memtype_write_from_string(self):
        self.set_up()
        self.assertEqual(self.xa.memtype_write_from_string('flash'), Avr8Protocol.AVR8_MEMTYPE_FLASH_PAGE)
        self.assertEqual(self.xa.memtype_write_from_string('eeprom'), Avr8Protocol.AVR8_MEMTYPE_EEPROM_ATOMIC)
        self.assertEqual(self.xa.memtype_write_from_string('internal_sram'), Avr8Protocol.AVR8_MEMTYPE_SRAM)

    def test_setup_debug_session(self):
        self.set_up()
        self.xa.setup_debug_session(clkdeb=123, timers_run=False, clkprg=456)
        self.xa.protocol.set_byte.assert_called_with(Avr8Protocol.AVR8_CTXT_OPTIONS,
                                                     Avr8Protocol.AVR8_OPT_RUN_TIMERS,
                                                     False)
        self.xa.protocol.set_variant.assert_called_once_with(Avr8Protocol.AVR8_VARIANT_TINYX)
        self.xa.protocol.set_function.assert_called_once_with(Avr8Protocol.AVR8_FUNC_DEBUGGING)
        self.xa.protocol.set_interface.assert_called_once_with(Avr8Protocol.AVR8_PHY_INTF_PDI_1W)
        self.xa.protocol.set_le16.assert_called_once_with(Avr8Protocol.AVR8_CTXT_PHYSICAL,
                                                          Avr8Protocol.AVR8_PHY_XM_PDI_CLK, 123)

    def test_regfile_read(self):
        self.set_up()
        self.xa.protocol.regfile_read.return_value=bytearray(range(32))
        self.assertEqual(self.xa.regfile_read(), bytearray(range(32)))

    def test_regfile_write(self):
        self.set_up()
        self.xa.regfile_write(bytearray(range(32)))
        self.xa.protocol.regfile_write.assert_called_with(bytearray(range(32)))

    def test_statreg_read(self):
        self.set_up()
        self.xa.protocol.memory_read.return_value=bytearray([0x7F])
        self.assertEqual(self.xa.statreg_read(), b'\x7F')
        self.xa.protocol.memory_read.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM,
                                                            0x3F, 1)

    def test_statreg_write(self):
        self.set_up()
        self.xa.statreg_write(b'\x06')
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM,
                                                            0x3F, b'\x06')

    def test_stack_pointer_write(self):
        self.set_up()
        self.xa.stack_pointer_write('b\x23\x01')
        self.xa.protocol.memory_write.assert_called_with(Avr8Protocol.AVR8_MEMTYPE_SRAM, 0x3D, 'b\x23\x01')

    def test_hardware_breakpoint_set_fail(self):
        self.set_up()
        self.assertEqual(self.xa.hardware_breakpoint_set(2, 0x200),None)

    def test_hardware_breakpoint_set_right(self):
        self.set_up()
        self.xa.protocol.check_response.return_value = None
        self.assertEqual(self.xa.hardware_breakpoint_set(1, 0x200), None)
        self.xa.protocol.jtagice3_command_response.assert_called_with(bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_SET, Avr8Protocol.CMD_VERSION0, 1, 1]) +
            binary.pack_le32(0x200) +
            bytearray([3]))

    def test_hardware_breakpoint_clear_right(self):
        self.set_up()
        self.xa.protocol.check_response.return_value = None
        self.assertEqual(self.xa.hardware_breakpoint_clear(1), None)
        self.xa.protocol.jtagice3_command_response.assert_called_with(bytearray([Avr8Protocol.CMD_AVR8_HW_BREAK_CLEAR, Avr8Protocol.CMD_VERSION0, 1]))

    def test_switch_to_progmode(self):
        self.set_up()
        self.xa.switch_to_progmode()
        self.xa.protocol.assert_has_calls([call.detach(), call.enter_progmode()])

    def test_switch_to_debmode(self):
        self.set_up()
        self.xa.switch_to_debmode()
        self.xa.protocol.leave_progmode.assert_called_once_with()

    def test_attach(self):
        self.set_up()
        self.xa.attach()
        self.xa.protocol.attach.assert_called_once_with()

    def test_reactivate(self):
        self.set_up()
        self.xa.deactivate_physical = MagicMock()
        self.xa.activate_physical = MagicMock()
        self.xa.reactivate()
        self.xa.protocol.assert_has_calls([call.detach(), call.attach(), call.reset()])
        self.xa.deactivate_physical.assert_called_once_with()
        self.xa.activate_physical.assert_called_once_with()
