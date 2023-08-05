from framework.cansignal import Signal, SignalGroup
from framework.concurrentcanbox import SendControl
from framework.trigger import OnReceiveSignalTrigger, OnReceiveAnyMsgTrigger, OnReceiveMsgTrigger, \
    OnReceiveMsgExcludeIdsTrigger, OnKeyPressedTrigger, OnKeyReleaseTrigger, OnReceiveSignalGroupTrigger, \
    OnReceiveMsgIdsTrigger


class VirtualNode:

    def __init__(self, name, dbc):
        self.dbc = dbc
        self.name = name
        self.send_worker = None
        self.msg_triggers = []
        self.key_triggers = []

    def set_send_worker(self, send_worker):
        self.send_worker = send_worker

    def _check_send_id(self, frame_id):
        return frame_id in self.id_set()

    def _check_send_batch(self, batch):
        for can_msg in batch.can_msgs:
            if not self._check_send_id(can_msg.id):
                return False
        return True

    def id_set(self):
        return self.dbc.sender_name_to_frame_ids.get(self.name)

    def send(self, batch):
        if not self._check_send_batch(batch):
            raise
        control = SendControl(send_from=self.name)
        return self.send_worker.send(batch, control)

    def change(self, signal, value):
        pass

    def receive_msg(self, can_msg):
        for trigger in self.msg_triggers:
            if trigger.check(can_msg):
                trigger.do_it(can_msg)

    def on_receive_any_msg(self):
        trigger = OnReceiveAnyMsgTrigger(self)
        self.msg_triggers.append(trigger)
        return trigger

    def on_receive_msg_exclude_ids(self, *msg_ids):
        trigger = OnReceiveMsgExcludeIdsTrigger(self, msg_ids)
        self.msg_triggers.append(trigger)
        return trigger

    def on_receive_msg_ids(self, *msg_ids):
        trigger = OnReceiveMsgIdsTrigger(self, msg_ids)
        self.msg_triggers.append(trigger)
        return trigger

    def on_receive_msg(self, can_msg):
        trigger = OnReceiveMsgTrigger(self, can_msg)
        self.msg_triggers.append(trigger)
        return trigger

    def on_receive_signal(self, name, value):
        sig = Signal(self.dbc, name, value)
        trigger = OnReceiveSignalTrigger(self, sig)
        self.msg_triggers.append(trigger)
        return trigger

    def on_receive_signals(self, name_value_dict):
        sig_group = SignalGroup(self.dbc)
        for name, value in name_value_dict.items():
            sig_group.update_signal_value(name, value)
        trigger = OnReceiveSignalGroupTrigger(self, sig_group)
        self.msg_triggers.append(trigger)
        return trigger

    def receive_key_event(self, key_event):
        for trigger in self.key_triggers:
            if trigger.check(key_event):
                trigger.do_it(key_event)

    def on_key_pressed(self, key_name):
        trigger = OnKeyPressedTrigger(self, key_name)
        self.key_triggers.append(trigger)
        return trigger

    def on_key_released(self, key_name):
        trigger = OnKeyReleaseTrigger(self, key_name)
        self.key_triggers.append(trigger)
        return trigger
