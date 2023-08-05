class CanMsg:

    def __init__(self, id, data, count=1, interval=0):
        self.id = id
        self.data = data
        self.count = count
        self.interval = interval

    def __repr__(self):
        return "CanMsg(id: %s, data: %s, count: %s, interval: %s)" \
               % (hex(self.id), self.data, self.count, self.interval)

    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id and \
               self.data == other.data and \
               self.count == other.count and \
               self.interval == other.interval

    def __hash__(self):
        return self.id * 100 + self.count * 10 + self.interval

    def same_content(self, other):
        if other is None:
            return False
        return self.id == other.id and \
               self.data == other.data


class CanMsgBatch:

    def __init__(self, can_msg=None, loop_count=-1, loop_interval=0):
        self.can_msgs = [] if can_msg is None else [can_msg]
        self.loop_count = loop_count
        self.loop_interval = loop_interval

    def add(self, can_msg):
        self.can_msgs.append(can_msg)

    def __repr__(self):
        return "CanMsgBatch(can_msgs: %s, loop_count: %s, loop_interval: %s)" \
               % (self.can_msgs, self.loop_count, self.loop_interval)

    def __eq__(self, other):
        if other is None:
            return False
        return self.can_msgs == other.can_msgs and \
               self.loop_count == other.loop_count and \
               self.loop_interval == other.loop_interval

    def __hash__(self):
        return len(self.can_msgs) * 100 + self.loop_count * 10 + self.loop_interval