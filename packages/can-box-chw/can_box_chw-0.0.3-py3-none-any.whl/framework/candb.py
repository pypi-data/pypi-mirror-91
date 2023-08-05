class DBC:
    def __init__(self):
        self.nodes = set()
        self.frame_id_to_sender_names = dict()
        self.sender_name_to_frame_ids = dict()
        self.signal_name_to_frame_id = dict()
        self.signal_name_to_choices = dict()
        self.frame_id_to_interval = dict()
        self.frame_id_to_signal_names = dict()
        self.dbs = list()
        pass

    def _set_node_list(self, db):
        for node in db.nodes:
            self.nodes.add(node.name)

    def _set_frame_id_to_sender_names(self, db):
        for msg in db.messages:
            if msg.frame_id not in self.frame_id_to_sender_names.keys():
                self.frame_id_to_sender_names[msg.frame_id] = msg.senders

    def _set_sender_name_to_frame_ids(self, db):
        for msg in db.messages:
            senders = msg.senders
            for sender in senders:
                if self.sender_name_to_frame_ids.get(sender) is None:
                    self.sender_name_to_frame_ids[sender] = set()
                self.sender_name_to_frame_ids[sender].add(msg.frame_id)

    def _set_signal_name_to_frame_id(self, db):
        for msg in db.messages:
            for signal in msg.signals:
                sig_name = signal.name
                if self.signal_name_to_frame_id.get(sig_name) is None:
                    self.signal_name_to_frame_id[sig_name] = msg.frame_id

    def _set_signal_name_to_choices(self, db):
        for msg in db.messages:
            for signal in msg.signals:
                sig_name = signal.name
                choices = signal.choices
                if self.signal_name_to_choices.get(sig_name) is None:
                    self.signal_name_to_choices[sig_name] = choices

    def _set_frame_id_to_interval(self, db):
        for msg in db.messages:
            if self.frame_id_to_interval.get(msg.frame_id) is None:
                self.frame_id_to_interval[msg.frame_id] = msg.cycle_time

    def _set_frame_id_to_signal_names(self, db):
        for msg in db.messages:
            if self.frame_id_to_signal_names.get(msg.frame_id) is None:
                self.frame_id_to_signal_names[msg.frame_id] = set()
            for sig in msg.signals:
                sig_name = sig.name
                self.frame_id_to_signal_names[msg.frame_id].add(sig_name)

    def _create_attr(self, db):
        msgs = db.messages
        for msg in msgs:
            if msg.name not in self.__dict__.keys():
                self.__dict__[msg.name] = msg
            sigs = msg.signals
            for sig in sigs:
                if sig.name not in self.__dict__.keys():
                    self.__dict__[msg.name].__dict__[sig.name] = sig
                chs = sig.choices
                if chs is not None:
                    for val, name in chs.items():
                        name = name.replace(" ", "_")
                        name = name.replace("0", "Zero")
                        self.__dict__[msg.name].__dict__[sig.name].__dict__[name] = val

    def load(self, db):
        self.dbs.append(db)
        self._set_node_list(db)
        self._set_frame_id_to_sender_names(db)
        self._set_sender_name_to_frame_ids(db)
        self._set_signal_name_to_frame_id(db)
        self._set_signal_name_to_choices(db)
        self._set_frame_id_to_interval(db)
        self._set_frame_id_to_signal_names(db)
        self._create_attr(db)

    def check_signal_name(self, signal_name):
        return signal_name in self.signal_name_to_frame_id.keys()

    def find_choices_by_signal_name(self, signal_name):
        return self.signal_name_to_choices.get(signal_name)

    def find_msg_id_by_signal_name(self, signal_name):
        return self.signal_name_to_frame_id.get(signal_name)

    def find_msg_interval_by_msg_id(self, msg_id):
        return self.frame_id_to_interval.get(msg_id)

    def find_signal_names_by_msg_id(self, msg_id):
        return self.frame_id_to_signal_names.get(msg_id)

    def encode_message(self, msg_id, signal_name_to_value):
        ret = b'\x00'
        for db in self.dbs:
            data = db.encode_message(msg_id, signal_name_to_value)
            ret = (int.from_bytes(ret, 'big') | int.from_bytes(data, 'big')).to_bytes(max(len(ret), len(data)), 'big')
        return ret

    def decode_message(self, msg_id, data, decode_choices=False):
        signal_name_to_choice_or_value = {}
        for db in self.dbs:
            data_dict = db.decode_message(msg_id, data, decode_choices)
            signal_name_to_choice_or_value = dict(signal_name_to_choice_or_value, **data_dict)
        return signal_name_to_choice_or_value