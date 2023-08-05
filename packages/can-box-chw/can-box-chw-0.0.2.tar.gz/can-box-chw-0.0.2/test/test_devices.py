import time
import unittest
from unittest.case import TestCase

from devices.devices import ZlgDevice, DeviceResult
from framework.canfactory import create_batch_from_zcanpro_exporting_file
from framework.canmsg import CanMsgBatch, CanMsg, CanFrame


class TestZlgDevice(TestCase):

    def setUp(self):
        self.dev = ZlgDevice()
        self.dev.open()

    def tearDown(self):
        self.dev.close()

    def test_open_channel(self):
        self.assertEqual(DeviceResult.SUCCESS, self.dev.open_channel())

    @unittest.skip("connect the chn0 to another can end")
    def test_send(self):
        self.assertEqual(DeviceResult.SUCCESS, self.dev.open_channel())
        batch = create_batch_from_zcanpro_exporting_file("files/test_batch_1_msg.list")
        can_msg = batch.can_msgs[0]
        self.assertEqual(1, self.dev.send(can_msg))
        self.assertEqual(DeviceResult.SUCCESS, self.dev.close_channel())

    def test_send_to_myself(self):
        self.assertEqual(DeviceResult.SUCCESS, self.dev.open_channel())
        batch = create_batch_from_zcanpro_exporting_file("files/test_batch_1_msg.list")
        can_msg = batch.can_msgs[0]
        self.assertEqual(1, self.dev.send_to_myself(can_msg))
        self.assertEqual(DeviceResult.SUCCESS, self.dev.close_channel())

    def test_receive(self):
        self.assertEqual(DeviceResult.SUCCESS, self.dev.open_channel())
        batch = create_batch_from_zcanpro_exporting_file("files/test_batch_1_msg.list")
        can_msg = batch.can_msgs[0]
        self.assertEqual(1, self.dev.send_to_myself(can_msg))
        time.sleep(1)
        rec = self.dev.receive()
        rec_batch, rec_cnt = rec
        self.assertEqual(1, rec_cnt)
        mock_batch = CanMsgBatch(CanMsg(CanFrame(486, [0, 12, 0])))
        self.assertEqual(rec_batch, mock_batch)
        self.assertEqual(DeviceResult.SUCCESS, self.dev.close_channel())

    def test_receive_block(self):
        self.assertEqual(DeviceResult.SUCCESS, self.dev.open_channel())
        batch = create_batch_from_zcanpro_exporting_file("files/test_batch_1_msg.list")
        can_msg = batch.can_msgs[0]
        self.assertEqual(1, self.dev.send_to_myself(can_msg))
        time.sleep(1)
        rec = self.dev.receive_block()
        rec_batch, rec_cnt = rec
        self.assertEqual(1, rec_cnt)
        mock_batch = CanMsgBatch(CanMsg(CanFrame(486, [0, 12, 0])))
        self.assertEqual(rec_batch, mock_batch)
        self.assertEqual(DeviceResult.SUCCESS, self.dev.close_channel())

    def test_is_device_online(self):
        self.assertTrue(self.dev.is_device_online())


if __name__ == '__main__':
    suit = unittest.TestSuite()
    suit.addTest(TestZlgDevice())
    runner = unittest.TextTestRunner()
    runner.run(suit)
