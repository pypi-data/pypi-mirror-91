import threading
import time
from concurrent.futures import wait
from concurrent.futures.thread import ThreadPoolExecutor

import keyboard

from devices.devices import DeviceResult


class SendControl:

    def __init__(self, send_from=None, stop_sending_event=None):
        if stop_sending_event is None:
            stop_sending_event = threading.Event()
        self.stop_sending_event = stop_sending_event
        self.send_from = send_from


class SendHandle:

    msg_id_to_handle = dict()

    def __init__(self, batch, future):
        self.batch = batch
        self.future = future
        self.stop_sending_event = batch.control.stop_sending_event

    def stop_sending(self):
        self.future.cancel()
        self.stop_sending_event.set()
        SendHandle.remove_handle_on_flight(self)

    def after(self, sec=None):
        wait([self.future], sec)
        return self

    def stop_after(self, sec=None):
        wait([self.future], sec)
        self.stop_sending()

    def wait(self, sec=None):
        wait([self.future], timeout=sec)

    @staticmethod
    def add_handle_on_flight(handle):
        msg_id = handle.batch.can_msgs[0].id
        SendHandle.msg_id_to_handle[msg_id] = handle

    @staticmethod
    def remove_handle_on_flight(handle):
        msg_id = handle.batch.can_msgs[0].id
        SendHandle.msg_id_to_handle.pop(msg_id)

    @staticmethod
    def get_msg_id_on_flight(msg_id):
        return SendHandle.msg_id_to_handle.get(msg_id)


class BatchSendWorker:

    def __init__(self, device, bus):
        self.executor = ThreadPoolExecutor(max_workers=11)
        self.dispatch_future = None
        self.device = device
        self.bus = bus

    def _send_one_loop(self, batch):
        for can_msg in batch.can_msgs:
            # down the control to the msg
            can_msg.control = batch.control
            for cnt in range(can_msg.count):
                self.device.send(can_msg)
                self.bus.broadcast_msg(can_msg)
                time.sleep(can_msg.interval / 1000.0)
        time.sleep(batch.loop_interval / 1000.0)

    def _send_infinity(self, batch):
        # print("send_infinity: ", batch)
        while True:
            if batch.control.stop_sending_event.is_set():
                # print("stop_sending_infinity: ", batch)
                break
            self._send_one_loop(batch)

    def _send_count(self, batch):
        # print("send_count: ", batch)
        for cnt in range(batch.loop_count):
            if batch.control.stop_sending_event.is_set():
                # print("stop_sending_count: ", batch)
                break
            self._send_one_loop(batch)

    def _send_batch(self, batch):
        if batch.loop_count == -1:
            self._send_infinity(batch)
        elif batch.loop_count > 0:
            self._send_count(batch)

    def send(self, batch, control=None):
        if control is None:
            control = SendControl()
        batch.control = control
        handle = SendHandle.get_msg_id_on_flight(batch.can_msgs[0].id)
        if handle is not None:
            handle.stop_sending()

        future = self.executor.submit(self._send_batch, batch)
        handle = SendHandle(batch, future)
        SendHandle.add_handle_on_flight(handle)
        return handle

    def kill(self):
        self.executor.shutdown(wait=False)


class BatchReceiveWorker:

    def __init__(self, device, bus):
        self.device = device
        self.bus = bus
        self.stop_receiving_event = threading.Event()
        self.receive_executor = ThreadPoolExecutor(1)

    def _receive(self):
        while True:
            batch, cnt = self.device.receive_block(1)
            if self.stop_receiving_event.is_set():
                break
            elif cnt > 0:
                batch.control = SendControl()
                for can_msg in batch.can_msgs:
                    can_msg.control = batch.control
                    self.bus.broadcast_msg(can_msg)

    def receive(self):
        self.receive_executor.submit(self._receive)

    def stop_receiving(self):
        self.stop_receiving_event.set()


class KeyWorker:

    def __init__(self, bus):
        self.bus = bus
        self.stop_listening_event = threading.Event()
        self.receive_executor = ThreadPoolExecutor(1)

    def _listen(self):
        while True:
            # TODO: bug! if bock, no way to run into here
            if self.stop_listening_event.is_set():
                break
            event = keyboard.read_event(suppress=False)
            self.bus.broadcast_key_event(event)

    def start_listening(self):
        self.receive_executor.submit(self._listen)

    def stop_listening(self):
        self.stop_listening_event.set()


class ConcurrentCanBox:

    def __init__(self, device):
        self.device = device
        self.device_open_flag = False
        self.channel_open_flag = False
        self.send_worker = BatchSendWorker(device)

    def open(self):
        if not self.device_open_flag:
            ret = self.device.open()
            self.send_worker = BatchSendWorker(self.device)
            self.device_open_flag = True
            return ret == DeviceResult.SUCCESS

    def send(self, batch):
        return self.send_worker.send(batch)

    def open_channel(self):
        if not self.channel_open_flag:
            ret = self.device.open_channel()
            self.channel_open_flag = True
            return ret == DeviceResult.SUCCESS

        return False

    def close_channel(self):
        if self.channel_open_flag:
            ret = self.device.close_channel()
            self.channel_open_flag = False
            return ret == DeviceResult.SUCCESS

        return False

    def close(self):
        if self.device_open_flag:
            self.close_channel()
            self.send_worker.kill()
            ret = self.device.close()
            self.device_open_flag = False
            return ret == DeviceResult.SUCCESS
