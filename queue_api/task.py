from email.policy import default
import uuid

class Task:
    """Class to represent Task entity"""
    def __init__(self, data, type):
        self.id = str(uuid.uuid4())
        self.data = data
        self.type = type
        self.status = 'not_started'
        match type:
            case 'reverse':
                self.interval = 2
                self.func = lambda : self.data[::-1]
            case 'pairwise_permutation':
                self.interval = 20
                self.func = lambda : ''.join([ self.data[x:x+2][::-1] for x in range(0, len(self.data), 2) ])
            case 'dup_by_idx':
                self.interval = 10
                self.func = lambda : ''.join(([x*(ind+1) if ind!=0 else x for ind, x in enumerate(self.data)]))
    """
        Process task data with its type
    """
    def do_func(self):
        self.data = self.func()