import json

from framework.canmsg import CanMsgBatch, CanMsg


def create_batch_from_zcanpro_exporting_file(path):
    """
    create CanMsgBatch by turn_light.list
    :param path: the absolute path for turn_light.list which is exported from DBC sending module in ZCanPro
    :return: CanMsgBatch instance
    """

    with open(path) as df:
        batch_obj = json.load(df)
        batch = CanMsgBatch()
        batch.loop_count = batch_obj["sendLoopCnt"]
        batch.loop_interval = batch_obj["sendLoopInterval"]
        batch.can_msgs = []
        can_msg_obj_list = batch_obj["msgList"]
        for can_msg_obj in can_msg_obj_list:
            count = can_msg_obj["sendCnt"]
            interval = can_msg_obj["sendInterval"]
            id = can_msg_obj["msgID"]
            data = can_msg_obj["datas"]
            can_msg = CanMsg(id, data, count, interval)
            batch.can_msgs.append(can_msg)

    raise_if_bad_batch(batch)
    return batch


def raise_if_bad_batch(batch):
    if batch is None:
        raise
    can_msgs = batch.can_msgs
    if len(can_msgs) == 0:
        raise

    tmp_id = -1
    for can_msg in can_msgs:
        frame_id = can_msg.id
        if tmp_id == -1:
            tmp_id = frame_id
        elif tmp_id != frame_id:
            raise


def generate_zcanpro_import_file_from_can_msg_batch(batch):
    """
    create turn_light.list which is used by ZCanPro DBC sending module from CanMsgBatch instance
    :param batch: CanMsgBatch
    :return: turn_light.list which is used by ZCanPro DBC sending module
    """
    pass


def create_batch_from_zcanpro_receive(zcanpro_rec_msgs, act_cnt):
    batch = CanMsgBatch()
    batch.can_msgs = []
    for i in range(act_cnt):
        zcanpro_rec_msg = zcanpro_rec_msgs[i]
        zframe = zcanpro_rec_msg.frame
        zcan_id = zframe.can_id
        zcan_dlc = zframe.can_dlc
        zdata = zframe.data[:zcan_dlc]
        can_msg = CanMsg(zcan_id, zdata)
        batch.can_msgs.append(can_msg)

    return batch


def create_batch_from_signal_group(*signal_groups, count=1, loop_count=-1):
    batch = CanMsgBatch()
    for group in signal_groups:
        can_msg = CanMsg(id=group.msg_id, data=group.to_data(), count=count, interval=group.interval)
        batch.add(can_msg)
    batch.loop_count = loop_count
    batch.loop_interval = batch.can_msgs[0].interval
    return batch


def create_can_msg_from_signal_group(signal_group):
    return CanMsg(id=signal_group.msg_id, data=signal_group.to_data(), count=1, interval=signal_group.interval)


if __name__ == '__main__':
    create_batch_from_zcanpro_exporting_file("../test/dbc.list")