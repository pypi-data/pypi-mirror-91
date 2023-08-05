import time

from devices.zlg.zlgcan import ZCAN, ZCAN_CHANNEL_INIT_CONFIG, ZCAN_TYPE_CAN, ZCAN_Transmit_Data

if __name__ == '__main__':
    _zcan = ZCAN()
    _dev_handle = _zcan.OpenDevice(device_type=4, device_index=0, reserved=0)
    print("_device_handle: ", _dev_handle)

    chn_cfg = ZCAN_CHANNEL_INIT_CONFIG()
    chn_cfg.can_type = ZCAN_TYPE_CAN
    chn_cfg.config.can.timing0 = 0
    chn_cfg.config.can.timing1 = 0x1C
    chn_cfg.config.can.acc_code = 0
    chn_cfg.config.can.acc_mask = 0xFFFFFFFF

    _can_handle_0 = _zcan.InitCAN(device_handle=_dev_handle, can_index=0, init_config=chn_cfg)
    print("_can_handle_0: ", _can_handle_0)

    ret = _zcan.StartCAN(_can_handle_0)
    print("_can_handle_0 StartCAN ret: (1是OK)", ret)

    _can_handle_1 = _zcan.InitCAN(device_handle=_dev_handle, can_index=1, init_config=chn_cfg)
    print("_can_handle_1: ", _can_handle_1)

    ret = _zcan.StartCAN(_can_handle_1)
    print("_can_handle_1 StartCAN ret: (1是OK)", ret)



    msg = ZCAN_Transmit_Data()
    msg.frame.can_id = 0x100
    msg.frame.rtr = 0
    msg.frame.eff = 0
    msg.frame.can_dlc = 8
    msg.frame.data[0] = 1
    msg.frame.data[1] = 1
    msg.frame.data[2] = 2
    msg.frame.data[3] = 3
    msg.frame.data[4] = 5
    msg.frame.data[5] = 8
    msg.frame.data[6] = 0xA
    msg.frame.data[7] = 0xF

    _send_num = 1
    _send_msgs = (ZCAN_Transmit_Data * _send_num)()
    _send_msgs[0] = msg

    trans_success_count = _zcan.Transmit(_can_handle_0, _send_msgs, _send_num)
    print("trans_success_count: ", trans_success_count)

    rec_num = _zcan.GetReceiveNum(_can_handle_1, ZCAN_TYPE_CAN)
    print("rec_num: ", rec_num)

    MAX_RCV_NUM = 10
    read_cnt = MAX_RCV_NUM if rec_num >= MAX_RCV_NUM else rec_num
    receive_msgs, act_num = _zcan.Receive(_can_handle_1, read_cnt)
    msg = receive_msgs[0].frame
    readable_data = ''.join(hex(msg.data[i])[2:] + ' ' for i in range(msg.can_dlc))
    print("readable_data: ", readable_data, " act_num: ", act_num)




    print("After 3s, close chn automatically")
    time.sleep(3)

    ret = _zcan.ResetCAN(_can_handle_0)
    print("_can_handle_0 ResetCAN ret: (1是OK)", ret)

    ret = _zcan.ResetCAN(_can_handle_1)
    print("_can_handle_1 ResetCAN ret: (1是OK)", ret)

    ret = _zcan.CloseDevice(_dev_handle)
    print("CloseDevice ret: (1是OK)", ret)

