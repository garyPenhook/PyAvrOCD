"""
Tests for tinyAVR UPDI device info registration.
"""
from unittest import TestCase

from pyavrocd.deviceinfo.devices.alldevices import dev_id, dev_iface, dev_name
from pyavrocd.deviceinfo.devices.attiny202 import DEVICE_INFO as ATTINY202
from pyavrocd.deviceinfo.devices.attiny204 import DEVICE_INFO as ATTINY204
from pyavrocd.deviceinfo.devices.attiny212 import DEVICE_INFO as ATTINY212
from pyavrocd.deviceinfo.devices.attiny214 import DEVICE_INFO as ATTINY214
from pyavrocd.deviceinfo.devices.attiny1604 import DEVICE_INFO as ATTINY1604
from pyavrocd.deviceinfo.devices.attiny1606 import DEVICE_INFO as ATTINY1606
from pyavrocd.deviceinfo.devices.attiny1607 import DEVICE_INFO as ATTINY1607
from pyavrocd.deviceinfo.devices.attiny1614 import DEVICE_INFO as ATTINY1614
from pyavrocd.deviceinfo.devices.attiny1616 import DEVICE_INFO as ATTINY1616
from pyavrocd.deviceinfo.devices.attiny1617 import DEVICE_INFO as ATTINY1617
from pyavrocd.deviceinfo.devices.attiny1624 import DEVICE_INFO as ATTINY1624
from pyavrocd.deviceinfo.devices.attiny1626 import DEVICE_INFO as ATTINY1626
from pyavrocd.deviceinfo.devices.attiny1627 import DEVICE_INFO as ATTINY1627
from pyavrocd.deviceinfo.devices.attiny402 import DEVICE_INFO as ATTINY402
from pyavrocd.deviceinfo.devices.attiny404 import DEVICE_INFO as ATTINY404
from pyavrocd.deviceinfo.devices.attiny406 import DEVICE_INFO as ATTINY406
from pyavrocd.deviceinfo.devices.attiny412 import DEVICE_INFO as ATTINY412
from pyavrocd.deviceinfo.devices.attiny414 import DEVICE_INFO as ATTINY414
from pyavrocd.deviceinfo.devices.attiny416 import DEVICE_INFO as ATTINY416
from pyavrocd.deviceinfo.devices.attiny417 import DEVICE_INFO as ATTINY417
from pyavrocd.deviceinfo.devices.attiny424 import DEVICE_INFO as ATTINY424
from pyavrocd.deviceinfo.devices.attiny426 import DEVICE_INFO as ATTINY426
from pyavrocd.deviceinfo.devices.attiny427 import DEVICE_INFO as ATTINY427
from pyavrocd.deviceinfo.devices.attiny804 import DEVICE_INFO as ATTINY804
from pyavrocd.deviceinfo.devices.attiny806 import DEVICE_INFO as ATTINY806
from pyavrocd.deviceinfo.devices.attiny807 import DEVICE_INFO as ATTINY807
from pyavrocd.deviceinfo.devices.attiny814 import DEVICE_INFO as ATTINY814
from pyavrocd.deviceinfo.devices.attiny816 import DEVICE_INFO as ATTINY816
from pyavrocd.deviceinfo.devices.attiny817 import DEVICE_INFO as ATTINY817
from pyavrocd.deviceinfo.devices.attiny824 import DEVICE_INFO as ATTINY824
from pyavrocd.deviceinfo.devices.attiny826 import DEVICE_INFO as ATTINY826
from pyavrocd.deviceinfo.devices.attiny827 import DEVICE_INFO as ATTINY827
from pyavrocd.deviceinfo.devices.attiny3216 import DEVICE_INFO as ATTINY3216
from pyavrocd.deviceinfo.devices.attiny3217 import DEVICE_INFO as ATTINY3217
from pyavrocd.deviceinfo.devices.attiny3224 import DEVICE_INFO as ATTINY3224
from pyavrocd.deviceinfo.devices.attiny3226 import DEVICE_INFO as ATTINY3226
from pyavrocd.deviceinfo.devices.attiny3227 import DEVICE_INFO as ATTINY3227


class TestTinyUpdiDeviceInfo(TestCase):
    """Verify tinyAVR UPDI devices are registered with the expected pack data."""

    def test_tiny_updi_parts_are_registered(self):
        """Every supported tinyAVR UPDI part should be discoverable by ID and name."""
        expected = {
            'attiny202': 0x1E9123,
            'attiny204': 0x1E9122,
            'attiny212': 0x1E9121,
            'attiny214': 0x1E9120,
            'attiny1604': 0x1E9425,
            'attiny1606': 0x1E9424,
            'attiny1607': 0x1E9423,
            'attiny1614': 0x1E9422,
            'attiny1616': 0x1E9421,
            'attiny1617': 0x1E9420,
            'attiny1624': 0x1E942A,
            'attiny1626': 0x1E9429,
            'attiny1627': 0x1E9428,
            'attiny402': 0x1E9227,
            'attiny404': 0x1E9226,
            'attiny406': 0x1E9225,
            'attiny412': 0x1E9223,
            'attiny414': 0x1E9222,
            'attiny416': 0x1E9221,
            'attiny417': 0x1E9220,
            'attiny424': 0x1E922C,
            'attiny426': 0x1E922B,
            'attiny427': 0x1E922A,
            'attiny804': 0x1E9325,
            'attiny806': 0x1E9324,
            'attiny807': 0x1E9323,
            'attiny814': 0x1E9322,
            'attiny816': 0x1E9321,
            'attiny817': 0x1E9320,
            'attiny824': 0x1E9329,
            'attiny826': 0x1E9328,
            'attiny827': 0x1E9327,
            'attiny3216': 0x1E9521,
            'attiny3217': 0x1E9522,
            'attiny3224': 0x1E9528,
            'attiny3226': 0x1E9527,
            'attiny3227': 0x1E9526,
        }
        for name, device_id in expected.items():
            self.assertEqual(dev_id[name], device_id)
            self.assertEqual(dev_iface[device_id], 'UPDI')
            self.assertEqual(dev_name[device_id], name)

    def test_tiny_updi_memory_layout_matches_pack(self):
        """Pack-derived memory layout constants should match the generated device tables."""
        for device in [
            ATTINY202, ATTINY204, ATTINY212, ATTINY214,
            ATTINY1604, ATTINY1606, ATTINY1607,
            ATTINY1614, ATTINY1616, ATTINY1617,
            ATTINY1624, ATTINY1626, ATTINY1627,
            ATTINY402, ATTINY404, ATTINY406,
            ATTINY412, ATTINY414, ATTINY416, ATTINY417,
            ATTINY424, ATTINY426, ATTINY427,
            ATTINY804, ATTINY806, ATTINY807,
            ATTINY814, ATTINY816, ATTINY817,
            ATTINY824, ATTINY826, ATTINY827,
            ATTINY3216, ATTINY3217, ATTINY3224, ATTINY3226, ATTINY3227
        ]:
            self.assertEqual(device['architecture'], 'avr8x')
            self.assertEqual(device['interface'], 'UPDI')
            self.assertEqual(device['flash_address_byte'], 0x00008000)
            self.assertEqual(device['prog_clock_khz'], 900)
            self.assertEqual(device['hv_implementation'], 0)

        for device in [ATTINY202, ATTINY204, ATTINY212, ATTINY214]:
            self.assertEqual(device['flash_size_bytes'], 0x800)
            self.assertEqual(device['flash_page_size_bytes'], 0x40)
            self.assertEqual(device['eeprom_size_bytes'], 0x40)
            self.assertEqual(device['eeprom_page_size_bytes'], 0x20)
            self.assertEqual(device['internal_sram_address_byte'], 0x3F80)
            self.assertEqual(device['internal_sram_size_bytes'], 0x80)

        for device in [
            ATTINY1604, ATTINY1606, ATTINY1607,
            ATTINY1614, ATTINY1616, ATTINY1617,
            ATTINY1624, ATTINY1626, ATTINY1627
        ]:
            self.assertEqual(device['flash_size_bytes'], 0x4000)
            self.assertEqual(device['flash_page_size_bytes'], 0x40)
            self.assertEqual(device['eeprom_size_bytes'], 0x100)
            self.assertEqual(device['eeprom_page_size_bytes'], 0x20)

        for device in [
            ATTINY402, ATTINY404, ATTINY406,
            ATTINY412, ATTINY414, ATTINY416, ATTINY417,
            ATTINY424, ATTINY426, ATTINY427
        ]:
            self.assertEqual(device['flash_size_bytes'], 0x1000)
            self.assertEqual(device['flash_page_size_bytes'], 0x40)
            self.assertEqual(device['eeprom_size_bytes'], 0x80)
            self.assertEqual(device['eeprom_page_size_bytes'], 0x20)

        for device in [ATTINY402, ATTINY404, ATTINY406, ATTINY412, ATTINY414, ATTINY416, ATTINY417]:
            self.assertEqual(device['internal_sram_address_byte'], 0x3F00)
            self.assertEqual(device['internal_sram_size_bytes'], 0x100)

        for device in [ATTINY424, ATTINY426, ATTINY427, ATTINY804, ATTINY806, ATTINY807,
                       ATTINY814, ATTINY816, ATTINY817]:
            self.assertEqual(device['internal_sram_address_byte'], 0x3E00)
            self.assertEqual(device['internal_sram_size_bytes'], 0x200)

        for device in [ATTINY804, ATTINY806, ATTINY807, ATTINY814, ATTINY816, ATTINY817,
                       ATTINY824, ATTINY826, ATTINY827]:
            self.assertEqual(device['flash_size_bytes'], 0x2000)
            self.assertEqual(device['flash_page_size_bytes'], 0x40)
            self.assertEqual(device['eeprom_size_bytes'], 0x80)
            self.assertEqual(device['eeprom_page_size_bytes'], 0x20)

        for device in [ATTINY3216, ATTINY3217, ATTINY3224, ATTINY3226, ATTINY3227]:
            self.assertEqual(device['flash_size_bytes'], 0x8000)
            self.assertEqual(device['flash_page_size_bytes'], 0x80)
            self.assertEqual(device['eeprom_size_bytes'], 0x100)
            self.assertEqual(device['eeprom_page_size_bytes'], 0x40)

        for device in [ATTINY1604, ATTINY1606, ATTINY1607]:
            self.assertEqual(device['internal_sram_address_byte'], 0x3C00)
            self.assertEqual(device['internal_sram_size_bytes'], 0x400)

        for device in [ATTINY824, ATTINY826, ATTINY827]:
            self.assertEqual(device['internal_sram_address_byte'], 0x3C00)
            self.assertEqual(device['internal_sram_size_bytes'], 0x400)

        for device in [ATTINY1614, ATTINY1616, ATTINY1617, ATTINY1624, ATTINY1626, ATTINY1627]:
            self.assertEqual(device['internal_sram_address_byte'], 0x3800)
            self.assertEqual(device['internal_sram_size_bytes'], 0x800)

        self.assertEqual(ATTINY3217['internal_sram_size_bytes'], 0x800)
        self.assertEqual(ATTINY3227['internal_sram_size_bytes'], 0xC00)
