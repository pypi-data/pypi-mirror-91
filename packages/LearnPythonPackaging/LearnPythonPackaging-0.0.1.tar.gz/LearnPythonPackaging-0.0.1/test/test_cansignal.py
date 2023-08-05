from unittest import TestCase, TestSuite, TextTestRunner

import cantools

from framework.candb import DBC
from framework.canfactory import create_batch_from_signal_group
from framework.cansignal import Signal, SignalGroup


class TestCanSignal(TestCase):

    def setUp(self):
        self.dbc = DBC()
        pdcu_db = cantools.db.load_file('../file/pdcu.dbc', database_format='dbc')
        ddcu_db = cantools.db.load_file('../file/ddcu.dbc', database_format='dbc')
        self.dbc.load(pdcu_db)
        self.dbc.load(ddcu_db)

    def tearDown(self):
        pass

    def test_001_create_signal(self):
        sig_name = "PDCU_MemoryMode"
        sig = Signal(dbc=self.dbc,
                     name=sig_name,
                     curr_value=self.dbc.PDCU_2.PDCU_MemoryMode.Read)
        print(sig)

    def test_002_create_signal_group(self):
        sig1 = Signal(dbc=self.dbc,
                     name="PDCU_MemoryMode",
                     curr_value=self.dbc.PDCU_2.PDCU_MemoryMode.Read)
        sig2 = Signal(dbc=self.dbc,
                     name="PDCU_MemoryResult",
                     curr_value=self.dbc.PDCU_2.PDCU_MemoryResult.Invalid_value)
        sg = SignalGroup(self.dbc, sig1, sig2)
        print(sg)

    def test_003_signal_group_to_data(self):
        sig1 = Signal(dbc=self.dbc,
                      name="PDCU_MemoryMode",
                      curr_value=self.dbc.PDCU_2.PDCU_MemoryMode.Read)
        sig2 = Signal(dbc=self.dbc,
                      name="PDCU_MemoryResult",
                      curr_value=self.dbc.PDCU_2.PDCU_MemoryResult.Invalid_value)
        sg = SignalGroup(self.dbc, sig1, sig2)
        print(sg.to_data())

    def test_003_signal_group_update(self):
        sig1 = Signal(dbc=self.dbc,
                      name="PDCU_MemoryMode",
                      curr_value=self.dbc.PDCU_2.PDCU_MemoryMode.Read)
        sig2 = Signal(dbc=self.dbc,
                      name="PDCU_MemoryResult",
                      curr_value=self.dbc.PDCU_2.PDCU_MemoryResult.Invalid_value)
        sg = SignalGroup(self.dbc, sig1, sig2)
        sg.update_signal_value("PDCU_MemoryResult", self.dbc.PDCU_2.PDCU_MemoryResult.Succeed)
        print(sg.to_data())
        print(sg.to_readable_data())

    def test_004_signal_group_clone(self):
        sig1 = Signal(dbc=self.dbc,
                      name="PDCU_MemoryMode",
                      curr_value=self.dbc.PDCU_2.PDCU_MemoryMode.Read)
        sig2 = Signal(dbc=self.dbc,
                      name="PDCU_MemoryResult",
                      curr_value=self.dbc.PDCU_2.PDCU_MemoryResult.Invalid_value)
        sg = SignalGroup(self.dbc, sig1, sig2)
        new_sg = sg.clone()
        new_sg.update_signal_value("PDCU_MemoryResult", self.dbc.PDCU_2.PDCU_MemoryResult.Succeed)
        print("sg: ", sg.to_readable_data())
        print("new_sg", new_sg.to_readable_data())

    def test_005_signal_group_to_batch(self):
        sig1 = Signal(dbc=self.dbc,
                      name="PDCU_MemoryMode",
                      curr_value=self.dbc.PDCU_2.PDCU_MemoryMode.Read)
        sig2 = Signal(dbc=self.dbc,
                      name="PDCU_MemoryResult",
                      curr_value=self.dbc.PDCU_2.PDCU_MemoryResult.Invalid_value)
        sg = SignalGroup(self.dbc, sig1, sig2)
        batch = create_batch_from_signal_group(sg)
        print(batch)


if __name__ == '__main__':
    suit = TestSuite()
    suit.addTest(TestCanSignal())
    runner = TextTestRunner()
    runner.run(suit)