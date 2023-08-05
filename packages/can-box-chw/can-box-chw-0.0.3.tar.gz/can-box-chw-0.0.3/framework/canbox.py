import threading
import time
from queue import Queue

from devices.devices import ZlgDevice, DeviceResult
from framework.canfactory import create_batch_from_zcanpro_exporting_file


class SendWorker(threading.Thread):

    def __init__(self, device):
        threading.Thread.__init__(self)
        self.queue = Queue()
        self.device = device
        self.stop_sending_event = threading.Event()

    def _send_one_loop(self, batch):
        to_myself = batch.to_myself
        for can_msg in batch.can_msgs:
            for cnt in range(can_msg.count):
                if to_myself:
                    self.device.send_to_myself(can_msg)
                else:
                    self.device.send(can_msg)
                time.sleep(can_msg.interval / 1000.0)
        time.sleep(batch.loop_interval / 1000.0)

    def _send_infinity(self, batch):
        while True:
            if self.stop_sending_event.is_set():
                break
            self._send_one_loop(batch)

    def _send_count(self, batch):
        for cnt in range(batch.loop_count):
            if self.stop_sending_event.is_set():
                break
            self._send_one_loop(batch)

    def run(self):
        while True:
            batch = self.queue.get()
            if batch is None:
                break
            while True:
                # if self.stop_sending_event.is_set():
                #     break
                if batch.loop_count == -1:
                    self._send_infinity(batch)
                    break
                elif batch.loop_count > 0:
                    self._send_count(batch)
                    break
                else:
                    raise

            self.stop_sending_event.clear()

    def send_batch(self, batch):
        self.queue.put(batch)

    def stop_sending(self):
        self.stop_sending_event.set()

    def kill(self):
        self.queue.put(None)
        self.join()


class ReceiveWorker(threading.Thread):

    def __init__(self, device, on_receive_fun):
        threading.Thread.__init__(self)
        self.device = device
        self.on_receive_fun = on_receive_fun
        self.stop_receiving_event = threading.Event()

    def run(self):
        while True:
            if self.stop_receiving_event.is_set():
                break
            batch, act_num = self.device.receive_block(1000)
            if act_num > 0 and self.on_receive_fun is not None:
                self.on_receive_fun(batch, act_num)

    def stop_receiving(self):
        self.stop_receiving_event.set()
        self.join()


class CanBox:

    def __init__(self, device):
        self.device_open_flag = False
        self.channel_open_flag = False
        self.device = device
        self.send_worker = None
        self.receive_worker = None

    def is_device_online(self):
        return self.device.is_device_online()

    def open(self, on_receive_callback=None):
        """
        open the device
        :return:
        """
        if not self.device_open_flag:
            ret = self.device.open()
            self.send_worker = SendWorker(self.device)
            self.receive_worker = ReceiveWorker(self.device, on_receive_callback)
            self.send_worker.start()
            self.receive_worker.start()
            self.device_open_flag = True
            return ret == DeviceResult.SUCCESS

        return False

    def open_channel(self):
        if not self.channel_open_flag:
            ret = self.device.open_channel()
            self.channel_open_flag = True
            return ret == DeviceResult.SUCCESS

        return False

    def send_batch(self, batch):
        batch.to_myself = False
        self.send_worker.send_batch(batch)

    def send_batch_to_myself(self, batch):
        batch.to_myself = True
        self.send_worker.send_batch(batch)

    def stop_sending(self):
        self.send_worker.stop_sending()

    def stop_receiving(self):
        self.receive_worker.stop_receiving()

    def close_channel(self):
        if self.channel_open_flag:
            self.send_worker.kill()
            ret = self.device.close_channel()
            self.channel_open_flag = False
            return ret == DeviceResult.SUCCESS

        return False

    def close(self):
        """
        close the device
        :return:
        """
        if self.device_open_flag:
            self.stop_sending()
            self.stop_receiving()
            self.close_channel()
            ret = self.device.close()
            self.device_open_flag = False
            return ret == DeviceResult.SUCCESS

        return False


if __name__ == '__main__':
    dev = ZlgDevice()
    cb = CanBox(dev)
    cb.open()
    cb.send_batch(create_batch_from_zcanpro_exporting_file("../test/dbc.list"))
    time.sleep(1)
    cb.stop_sending()
    cb.close()