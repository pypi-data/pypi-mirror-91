import unittest
from unittest.case import TestCase

from devices.devices import Device
from framework.canfactory import create_batch_from_zcanpro_exporting_file
from framework.concurrentcanbox import BatchSendWorker


class TestMultiCanBox(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_send_1_batch_10_loop(self):
        dev = Device()
        send_worker = BatchSendWorker(dev)
        batch = create_batch_from_zcanpro_exporting_file("files/test_multicanbox_1_msg_10_cnt.list")
        handle = send_worker.send(batch)
        handle.wait()

    def test_002_send_1_batch_infinity_loop(self):
        dev = Device()
        send_worker = BatchSendWorker(dev)
        batch = create_batch_from_zcanpro_exporting_file("files/test_multicanbox_1_msg_infinity_1.list")
        handle = send_worker.send(batch)
        handle.wait(5)
        handle.stop_sending()

    def test_003_send_2_batch(self):
        dev = Device()
        send_worker = BatchSendWorker(dev)
        handle_inf_1 = send_worker.send(create_batch_from_zcanpro_exporting_file("files/test_multicanbox_1_msg_infinity_1.list"))
        handle_inf_2 = send_worker.send(create_batch_from_zcanpro_exporting_file("files/test_multicanbox_1_msg_infinity_2.list"))
        handle_inf_1.wait(1)
        handle_inf_1.stop_sending()
        handle_inf_2.wait(3)

    def test_004_auto_stop_when_diff(self):
        dev = Device()
        send_worker = BatchSendWorker(dev)
        handle_ig_on = send_worker.send(
            create_batch_from_zcanpro_exporting_file("files/test_multicanbox_ig_on.list"),
            to_myself=False,
            auto_stop_sending_conflict_batch=False
        )
        handle_ig_on.after(1)

        handle_ig_off = send_worker.send(
            create_batch_from_zcanpro_exporting_file("files/test_multicanbox_ig_off.list"),
            to_myself=False,
            auto_stop_sending_conflict_batch=False)
        handle_ig_off.after(3).stop_sending()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestMultiCanBox())

    runner = unittest.TextTestRunner()
    runner.run(suite)
