import time
from abc import abstractmethod
from datetime import datetime

import keyboard


class SendOperation:

    def __init__(self, node):
        self.node = node

    def send(self, batch):
        self.node.send(batch)


class PrintOperation:

    def __init__(self, node):
        self.node = node

    def print(self, obj):
        t = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print("[%s] %s #print: %s" % (t, self.node.name, obj))


class PrintReadableMsgOperation:

    def __init__(self, node):
        self.node = node
        self.dbc = node.dbc

    def print_msg(self, can_msg):
        readable_msg = self.dbc.decode_message(can_msg.id, can_msg.data, True)
        t = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print("(%s) %s #print_msg: %s" % (t, self.node.name, readable_msg))


class WriteAscFileOperation:

    def __init__(self, node, file_path):
        self.node = node
        self.file_path = file_path
        self.start_time = None
        with open(self.file_path, "w") as f:
            f.write("")

    def write_asc_file(self, can_msg):
        if self.start_time is None:
            self.start_time = time.time()
        delta_time = time.time() - self.start_time
        can_id = hex(can_msg.id).replace("0x", "")
        dlc = len(can_msg.data)
        data = can_msg.data
        data_str = ""
        for d in data:
            data_str += str(hex(d)).replace("0x", "").zfill(2)
            data_str += " "
        asc_line = "%s 1 %s Rx d %s %s\n" % (format(delta_time, '.6f'), can_id, dlc, data_str)
        with open(self.file_path, "a") as f:
            print(asc_line)
            f.write(asc_line)


class FunctionOperation:

    def __init__(self, node, fun, *args):
        self.node = node
        self.fun = fun
        self.args = args

    def run(self):
        self.fun(*self.args)


class Trigger:

    def __init__(self, node):
        self.node = node
        self.to_do = None
        self.print_operation = None
        self.print_readable_msg_operation = None
        self.write_asc_file_operation = None
        self.send_operation = None
        self.function_operation = None

    @abstractmethod
    def check(self, can_msg):
        return True

    def do_it(self, obj):
        if self.to_do is not None:
            self.to_do(obj)

    def print(self):
        if self.print_operation is None:
            self.print_operation = PrintOperation(self.node)
        self.to_do = lambda obj: self.print_operation.print(obj)

    def print_msg(self):
        if self.print_readable_msg_operation is None:
            self.print_readable_msg_operation = PrintReadableMsgOperation(self.node)
        self.to_do = lambda can_msg: self.print_readable_msg_operation.print_msg(can_msg)

    def write_asc_file(self, file_path):
        if self.write_asc_file_operation is None:
            self.write_asc_file_operation = WriteAscFileOperation(self.node, file_path)
        self.to_do = lambda can_msg: self.write_asc_file_operation.write_asc_file(can_msg)

    def send(self, batch):
        if self.send_operation is None:
            self.send_operation = SendOperation(self.node)
        self.to_do = lambda not_used: self.send_operation.send(batch)

    def run(self, fun, *args):
        if self.function_operation is None:
            self.function_operation = FunctionOperation(self.node, fun, *args)
        self.to_do = lambda not_used: self.function_operation.run()


class OnReceiveAnyMsgTrigger(Trigger):

    def __init__(self, node):
        super().__init__(node)

    def check(self, can_msg):
        return True


class OnReceiveMsgExcludeIdsTrigger(Trigger):

    def __init__(self, node, exclude_ids):
        super().__init__(node)
        self.exclude_ids = exclude_ids

    def check(self, can_msg):
        return can_msg.id not in self.exclude_ids


class OnReceiveMsgIdsTrigger(Trigger):

    def __init__(self, node, ids):
        super().__init__(node)
        self.ids = ids

    def check(self, can_msg):
        return can_msg.id in self.ids


class OnReceiveMsgTrigger(Trigger):

    def __init__(self, node, can_msg):
        super().__init__(node)
        self.cared_can_msg = can_msg

    def check(self, can_msg):
        return self.cared_can_msg.same_content(can_msg)


class OnReceiveSignalTrigger(Trigger):

    def __init__(self, node, signal):
        super().__init__(node)
        self.signal = signal

    def check(self, can_msg):
        if can_msg.id == self.signal.msg_id:
            dbc = self.signal.dbc
            signal_name_to_value = dbc.decode_message(can_msg.id, can_msg.data)
            value = signal_name_to_value.get(self.signal.name)
            if value is None:
                raise
            if value == self.signal.curr_value:
                return True
        return False


class OnReceiveSignalGroupTrigger(Trigger):

    def __init__(self, node, signal_group):
        super().__init__(node)
        self.signal_group = signal_group

    def check(self, can_msg):
        if can_msg.id == self.signal_group.msg_id:
            dbc = self.signal_group.dbc
            signal_name_to_value = dbc.decode_message(can_msg.id, can_msg.data)
            for sig_name, sig in self.signal_group.items():
                if signal_name_to_value.get(sig_name) is None:
                    raise
                # print("sig_name: ", sig_name, "signal_name_to_value.get(sig_name): ", signal_name_to_value.get(sig_name), "sig.curr_value: ", sig.curr_value)
                if signal_name_to_value.get(sig_name) != sig.curr_value:
                    return False
            return True
        return False


class OnKeyPressedTrigger(Trigger):

    def __init__(self, node, key_name):
        super().__init__(node)
        self.key_name = key_name

    def check(self, key_event):
        return key_event.event_type == keyboard.KEY_DOWN and key_event.name == self.key_name


class OnKeyReleaseTrigger(Trigger):

    def __init__(self, node, key_name):
        super().__init__(node)
        self.key_name = key_name

    def check(self, key_event):
        return key_event.event_type == keyboard.KEY_UP and key_event.name == self.key_name