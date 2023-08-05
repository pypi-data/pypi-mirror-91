import time
from abc import abstractmethod

from devices.zlg.zlgcan import ZCAN, ZCAN_CHANNEL_INIT_CONFIG, ZCAN_TYPE_CAN, ZCAN_Transmit_Data, ZCAN_STATUS_ONLINE, \
    INVALID_DEVICE_HANDLE, INVALID_CHANNEL_HANDLE, ZCAN_STATUS_ERR, ZCAN_SEND_TYPE_NORMAL, \
    ZCAN_SEND_TYPE_SEND_TO_MYSELF
from framework.canfactory import create_batch_from_zcanpro_receive


class DeviceResult:
    SUCCESS = 0
    DEVICE_OPEN_FAIL = 1
    DEVICE_CLOSE_FAIL = 2
    CHANNEL_CONFIG_FAIL = 3
    CHANNEL_OPEN_FAIL = 4
    CHANNEL_CLOSE_FAIL = 5
    SEND_FAIL = 6


class Device:

    def __init__(self):
        self.send_success_count = 0
        self.rec_success_count = 0

    @abstractmethod
    def open(self):
        print("Device #open")
        return DeviceResult.SUCCESS

    @abstractmethod
    def is_device_online(self):
        print("Device #is_device_online")
        return True

    @abstractmethod
    def open_channel(self):
        print("Device #open_channel")
        return DeviceResult.SUCCESS

    @abstractmethod
    def send(self, can_msg):
        self.send_success_count += 1
        print("Device #send [count=%s]: %s" % (self.send_success_count, can_msg))
        pass

    @abstractmethod
    def receive(self):
        self.rec_success_count += 1
        print("Device #receive [count=%s]: " % (self.rec_success_count))


    @abstractmethod
    def receive_block(self, timeout=-1):
        self.rec_success_count += 1
        time.sleep(1)
        print("Device #receive [count=%s]: " % (self.rec_success_count))
        return None, 0

    @abstractmethod
    def close_channel(self):
        print("Device #close_channel")
        return DeviceResult.SUCCESS

    @abstractmethod
    def close(self):
        print("Device #close")
        return DeviceResult.SUCCESS


class ZlgDevice(Device):

    def __init__(self, zlgcan_dll):
        self.zcan = ZCAN(zlgcan_dll)
        self.dev_handle = INVALID_DEVICE_HANDLE
        self.chn_handle = INVALID_CHANNEL_HANDLE
        self.send_success_count = 0
        self.send_fail_count = 0
        self.rec_success_count = 0

    def open(self):
        self.dev_handle = self.zcan.OpenDevice(device_type=4, device_index=0, reserved=0)
        if self.dev_handle is INVALID_DEVICE_HANDLE:
            return DeviceResult.DEVICE_OPEN_FAIL

        return DeviceResult.SUCCESS

    def config(self):
        chn_cfg = ZCAN_CHANNEL_INIT_CONFIG()
        chn_cfg.can_type = ZCAN_TYPE_CAN
        chn_cfg.config.can.timing0 = 0
        chn_cfg.config.can.timing1 = 0x1C
        chn_cfg.config.can.acc_code = 0
        chn_cfg.config.can.acc_mask = 0xFFFFFFFF
        return chn_cfg

    def open_channel(self):
        chn_cfg = self.config()
        self.chn_handle = self.zcan.InitCAN(device_handle=self.dev_handle, can_index=0, init_config=chn_cfg)
        if self.chn_handle is INVALID_CHANNEL_HANDLE:
            return DeviceResult.CHANNEL_CONFIG_FAIL

        ret = self.zcan.StartCAN(self.chn_handle)
        if ret is ZCAN_STATUS_ERR:
            return DeviceResult.CHANNEL_OPEN_FAIL

        return DeviceResult.SUCCESS

    def is_device_online(self):
        return self.dev_handle is not None and \
               self.zcan.DeviceOnLine(self.dev_handle) == ZCAN_STATUS_ONLINE

    def send(self, can_msg, transmit_type=ZCAN_SEND_TYPE_NORMAL):
        if self.chn_handle is None:
            return DeviceResult.SEND_FAIL

        msg = ZCAN_Transmit_Data()
        msg.transmit_type = transmit_type
        msg.frame.can_id = can_msg.id
        msg.frame.rtr = 0
        msg.frame.eff = 0
        msg.frame.can_dlc = len(can_msg.data)
        for i in range(msg.frame.can_dlc):
            msg.frame.data[i] = can_msg.data[i]

        send_num = 1
        send_msgs = (ZCAN_Transmit_Data * send_num)()
        send_msgs[0] = msg

        trans_success_count = self.zcan.Transmit(self.chn_handle, send_msgs, send_num)
        return trans_success_count

    def send_to_myself(self, can_msg):
        return self.send(can_msg, transmit_type=ZCAN_SEND_TYPE_SEND_TO_MYSELF)

    def receive(self):
        rec_num = self.zcan.GetReceiveNum(self.chn_handle, ZCAN_TYPE_CAN)
        if rec_num > 0:
            MAX_RCV_NUM = 10
            read_cnt = MAX_RCV_NUM if rec_num >= MAX_RCV_NUM else rec_num
            receive_msgs, act_num = self.zcan.Receive(self.chn_handle, read_cnt)
            batch = create_batch_from_zcanpro_receive(receive_msgs, act_num)
            return batch, act_num
        return None, 0

    def receive_block(self, timeout=-1):
        read_cnt = 10
        receive_msgs, act_num = self.zcan.Receive(self.chn_handle, read_cnt, timeout)
        if act_num <= 0:
            return None, 0

        batch = create_batch_from_zcanpro_receive(receive_msgs, act_num)
        return batch, act_num

    def close_channel(self):
        if self.chn_handle is INVALID_CHANNEL_HANDLE:
            return DeviceResult.CHANNEL_CLOSE_FAIL

        ret = self.zcan.ResetCAN(self.chn_handle)
        if ret is ZCAN_STATUS_ERR:
            return DeviceResult.CHANNEL_CLOSE_FAIL

        return DeviceResult.SUCCESS

    def close(self):
        if self.dev_handle is INVALID_DEVICE_HANDLE:
            return DeviceResult.DEVICE_CLOSE_FAIL

        ret = self.zcan.CloseDevice(self.dev_handle)
        if ret is ZCAN_STATUS_ERR:
            return DeviceResult.DEVICE_CLOSE_FAIL

        return DeviceResult.SUCCESS


# DEVICE = Device()
# ZLG_DEVICE = ZlgDevice("../devices/zlg/zlgcan.dll")