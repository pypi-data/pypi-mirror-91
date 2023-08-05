import time
import unittest
from unittest import TestCase

from devices.devices import ZlgDevice
from framework.canbox import CanBox
from framework.canfactory import create_batch_from_zcanpro_exporting_file
from framework.canmsg import CanMsgBatch, CanMsg


class TestCanBox(TestCase):

    def setUp(self):
        dev = ZlgDevice()
        self.can_box = CanBox(dev)

    def tearDown(self):
        pass

    def test_open_and_close_device(self):
        self.assertTrue(self.can_box.open())
        self.assertTrue(self.can_box.close())

    def test_open_and_close_channel(self):
        self.assertTrue(self.can_box.open())
        self.assertTrue(self.can_box.open_channel())
        self.assertTrue(self.can_box.close_channel())
        self.assertTrue(self.can_box.close())

    def test_device_online(self):
        self.assertTrue(self.can_box.open())
        self.assertTrue(self.can_box.is_device_online())
        self.assertTrue(self.can_box.close())
        self.assertFalse(self.can_box.is_device_online())

    def test_send_batch_1(self):
        def on_receive(rec_batch, act_cnt):
            mock_batch = CanMsgBatch(CanMsg(486, [0, 12, 0]))
            self.assertEqual(1, act_cnt)
            self.assertEqual(mock_batch, rec_batch)

        self.assertTrue(self.can_box.open(on_receive))
        self.assertTrue(self.can_box.open_channel())
        self.can_box.send_batch_to_myself(create_batch_from_zcanpro_exporting_file("files/test_batch_1_msg.list"))
        self.assertTrue(self.can_box.close_channel())
        self.assertTrue(self.can_box.close())

    def test_send_batch_2(self):
        def on_receive(rec_batch, act_cnt):
            m1 = CanMsg(486, [0, 12, 0])
            m2 = CanMsg(464, [8, 0, 0, 0, 0, 0, 0, 0])
            m3 = CanMsg(514, [0, 0, 0, 0, 0, 0, 0, 0])
            ms = [m1, m2, m3]
            mock_batch = CanMsgBatch()
            mock_batch.can_msg = ms
            # self.assertEqual(mock_batch, rec_batch)
            # self.assertEqual(1, act_cnt)
            # print(rec_batch)

        self.assertTrue(self.can_box.open(on_receive))
        self.assertTrue(self.can_box.open_channel())
        self.can_box.send_batch_to_myself(create_batch_from_zcanpro_exporting_file("files/test_batch_3_msgs.list"))
        time.sleep(5)
        self.assertTrue(self.can_box.close_channel())
        self.assertTrue(self.can_box.close())


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestCanBox())

    runner = unittest.TextTestRunner()
    runner.run(suite)
