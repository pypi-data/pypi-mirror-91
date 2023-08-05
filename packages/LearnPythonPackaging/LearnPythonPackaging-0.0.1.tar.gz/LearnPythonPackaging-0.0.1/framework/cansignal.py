class Signal:

    def __init__(self, dbc, name=None, curr_value=None):
        if not dbc.check_signal_name(name):
            raise
        choices = dbc.find_choices_by_signal_name(name)
        if choices is not None:
            if curr_value not in choices.keys():
                raise
        self.name = name
        self.curr_value = curr_value
        self.value_to_choice = choices
        self.msg_id = dbc.find_msg_id_by_signal_name(name)
        self.dbc = dbc

    def __repr__(self):
        return "Signal(msg_id: %s, name: %s, curr_value: %s, value_to_choice: %s)" \
               % (self.msg_id, self.name, self.curr_value, self.value_to_choice)

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name and self.curr_value == other.curr_value

    def __hash__(self):
        return hash(self.name) + hash(self.curr_value)


class SignalGroup:

    def __init__(self, dbc, *sigs):
        self._missing_signal_init_flag = False
        self.dbc = dbc
        self.msg_id = None
        self.signals = dict()
        self.interval = None
        if sigs is not None:
            for sig in sigs:
                self.update(sig)

    def init_missing_sig_as_default_value(self):
        # we add missing signal value to default 0,
        # event if we call add after creation of signal_group, new signal push out the old one
        for sig_name in self.dbc.find_signal_names_by_msg_id(self.msg_id):
            if self.signals.get(sig_name) is None:
                self.update(Signal(self.dbc, sig_name, 0))

    def update(self, signal):
        if signal is None:
            raise
        if len(self.signals) > 0 and signal.msg_id != self.msg_id:
            raise
        self.signals[signal.name] = signal

        if not self._missing_signal_init_flag:
            self.msg_id = signal.msg_id
            self.interval = self.dbc.find_msg_interval_by_msg_id(self.msg_id)
            self.init_missing_sig_as_default_value()
            self._missing_signal_init_flag = True


    def update_signal_value(self, name, curr_value):
        self.update(Signal(self.dbc, name, curr_value))

    def clone(self):
        return SignalGroup(self. dbc, *self.signals.values())

    def to_data(self):
        signal_name_to_value = {sig.name: sig.curr_value for sig in self.signals.values()}
        data_bytes = self.dbc.encode_message(self.msg_id, signal_name_to_value)
        return list(data_bytes)

    def to_readable_data(self):
        return self.dbc.decode_message(self.msg_id, self.to_data(), True)

    def items(self):
        return self.signals.items()

    def __repr__(self):
        return "SignalGroup(msg_id: %s, interval: %s, signals: %s)" \
               % (self.msg_id, self.interval, self.signals)

