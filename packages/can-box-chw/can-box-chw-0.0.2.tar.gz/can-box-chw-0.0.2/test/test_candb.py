from unittest.case import TestCase

import cantools

from framework.candb import DBC


class TestDBC(TestCase):

    def setUp(self):
        dbc = DBC()
        pdcu_db = cantools.db.load_file('../file/pdcu.dbc', database_format='dbc')
        ddcu_db = cantools.db.load_file('../file/ddcu.dbc', database_format='dbc')
        dbc.load(pdcu_db)
        dbc.load(ddcu_db)
        self.dbc = dbc
        self.pdcu_db = pdcu_db
        pass

    def tearDown(self):
        pass

    def test_001_load_two_dbc_files(self):
        dbc = self.dbc
        self.assertEqual("PDCU_2", dbc.PDCU_2.name)
        self.assertEqual("PDCU_MemoryMode", dbc.PDCU_2.PDCU_MemoryMode.name)
        self.assertEqual(0, dbc.PDCU_2.PDCU_MemoryMode.Memory)
        self.assertEqual(1, dbc.PDCU_2.PDCU_MemoryMode.Read)
        self.assertEqual(2, dbc.PDCU_2.PDCU_MemoryMode.Init)
        self.assertEqual(3, dbc.PDCU_2.PDCU_MemoryMode.No_action)

        self.assertEqual("DDCU_2", dbc.DDCU_2.name)
        self.assertEqual("DDCU_MemoryMode", dbc.DDCU_2.DDCU_MemoryMode.name)
        self.assertEqual(0, dbc.DDCU_2.DDCU_MemoryMode.Memory)
        self.assertEqual(1, dbc.DDCU_2.DDCU_MemoryMode.Read)
        self.assertEqual(2, dbc.DDCU_2.DDCU_MemoryMode.Init)
        self.assertEqual(3, dbc.DDCU_2.DDCU_MemoryMode.No_action)

    def test_002_decode(self):
        data = [0x21, 0x03, 0, 0, 0, 0, 0, 0]
        ret = self.pdcu_db.decode_message(frame_id_or_name=488, data=data, decode_choices=False)
        print(ret)

        ret_2 = self.pdcu_db.encode_message(frame_id_or_name=488, data=ret)
        # print(ret_2)
        self.assertEqual(list(ret_2), data)


