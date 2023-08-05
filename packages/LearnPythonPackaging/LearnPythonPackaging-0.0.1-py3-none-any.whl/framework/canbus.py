from concurrent.futures.thread import ThreadPoolExecutor

from framework.concurrentcanbox import BatchSendWorker, BatchReceiveWorker, KeyWorker


class Bus:

    def __init__(self, device):
        self.start_flag = False
        self.device = device
        self.node_list = []
        self.executor = ThreadPoolExecutor()
        self.send_worker = BatchSendWorker(device=device, bus=self)
        self.receive_worker = BatchReceiveWorker(device=device, bus=self)
        self.key_worker = KeyWorker(bus=self)

    def start(self):
        self.device.open()
        self.device.open_channel()
        self.receive_worker.receive()
        # self.key_worker.start_listening()
        self.start_flag = True

    def stop(self):
        self.device.close_channel()
        self.device.close()
        self.receive_worker.stop_receiving()
        # self.key_worker.stop_listening()
        self.start_flag = False

    def register(self, node):
        if self.start_flag:
            raise RuntimeError("Can not register node after but called start")
        if node is not None:
            self.node_list.append(node)
            node.set_send_worker(self.send_worker)

    def _broadcast_msg(self, can_msg):
        for node in self.node_list:
            if node.name != can_msg.control.send_from:
                node.receive_msg(can_msg)

    def broadcast_msg(self, can_msg):
        self.executor.submit(self._broadcast_msg, can_msg)

    def _broadcast_key_event(self, key_event):
        for node in self.node_list:
            node.receive_key_event(key_event)

    def broadcast_key_event(self, key_event):
        self.executor.submit(self._broadcast_key_event, key_event)