import unittest
from unittest.case import TestCase

import cantools

from devices.devices import DEVICE
from framework.canbus import Bus
from framework.candb import DBC
from framework.canfactory import create_batch_from_zcanpro_exporting_file, \
    create_batch_from_signal_group, create_can_msg_from_signal_group
from framework.cansignal import Signal, SignalGroup
from framework.nodes import VirtualNode


class TestVirtualNode(TestCase):

    def setUp(self):
        dbc = DBC()
        bus = Bus(DEVICE)
        pdcu_db = cantools.db.load_file('../file/pdcu.dbc', database_format='dbc')
        ddcu_db = cantools.db.load_file('../file/ddcu.dbc', database_format='dbc')
        dbc.load(pdcu_db)
        dbc.load(ddcu_db)
        ddcu = VirtualNode("DriverDCU", dbc)
        pdcu = VirtualNode("PassengerDCU", dbc)
        dscu = VirtualNode("DSCU", dbc)
        logger = VirtualNode("logger", dbc)
        logger.on_receive_any_msg().print()
        bus.register(ddcu)
        bus.register(pdcu)
        bus.register(dscu)
        bus.register(logger)

        self.dbc = dbc
        self.pdcu = pdcu
        self.ddcu = ddcu
        self.dscu = dscu
        self.bus = bus
        pass

    def tearDown(self):
        pass

    def test_001_check_id(self):
        self.assertTrue(self.ddcu._check_send_id(0x1E6))
        self.assertEqual(self.pdcu.id_set(), {0x1E8, 0x1EA})

    def test_002_send_and_receive(self):
        self.bus.start()

        batch = create_batch_from_zcanpro_exporting_file("files/DDCU_1.list")
        handle_1 = self.ddcu.send(batch)
        batch = create_batch_from_zcanpro_exporting_file("files/PDCU_1.list")
        handle_2 = self.pdcu.send(batch)

        handle_1.after(2).stop_sending()
        handle_2.after(1).stop_sending()

        self.bus.stop()

    def test_003_trigger_on_receive_msg(self):
        self.bus.start()
        sig1 = Signal(dbc=self.dbc, name="DSCU_MemoryMode",
                      curr_value=self.dbc.DSCU_Cmd.DSCU_MemoryMode.Read)
        sig2 = Signal(dbc=self.dbc, name="DSCU_MemoryResult",
                      curr_value=self.dbc.DSCU_Cmd.DSCU_MemoryResult.Succeed)
        sg = SignalGroup(self.dbc, sig1, sig2)

        can_msg = create_can_msg_from_signal_group(sg)
        self.pdcu.on_receive_msg(can_msg).print()

        # sg = sg.clone()
        # sg.update_signal_value("DSCU_MemoryResult", self.dbc.DSCU_Cmd.DSCU_MemoryResult.Succeed)
        batch = create_batch_from_signal_group(sg)
        self.dscu.send(batch).after(1)

        self.bus.stop()

    def test_005_trigger(self):
        self.bus.start()
        sig1 = Signal(dbc=self.dbc, name="DSCU_MemoryMode",
                      curr_value=self.dbc.DSCU_Cmd.DSCU_MemoryMode.Read)
        sig2 = Signal(dbc=self.dbc, name="DSCU_MemoryResult",
                      curr_value=self.dbc.DSCU_Cmd.DSCU_MemoryResult.Succeed)
        sg = SignalGroup(self.dbc, sig1, sig2)

        batch = create_batch_from_signal_group(sg)
        self.dscu\
            .on_receive_signal(name="PDCU_MemoryResult", value=self.dbc.PDCU_2.PDCU_MemoryResult.Succeed)\
            .send(batch)

        sig1 = Signal(dbc=self.dbc, name="PDCU_MemoryMode",
                      curr_value=self.dbc.PDCU_2.PDCU_MemoryMode.Read)
        sig2 = Signal(dbc=self.dbc, name="PDCU_MemoryResult",
                      curr_value=self.dbc.PDCU_2.PDCU_MemoryResult.Invalid_value)
        sg = SignalGroup(self.dbc, sig1, sig2)
        batch = create_batch_from_signal_group(sg)
        self.pdcu.send(batch).after(1)

        sg = sg.clone()
        sg.update_signal_value(
            name="PDCU_MemoryResult",
            curr_value=self.dbc.PDCU_2.PDCU_MemoryResult.Succeed)

        batch = create_batch_from_signal_group(sg)
        self.pdcu.send(batch).after(1)

        self.bus.stop()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestVirtualNode())

    runner = unittest.TextTestRunner()
    runner.run(suite)