from queue import Queue
from abc import ABC, abstractmethod


class Resource(ABC):

    @abstractmethod
    def insert_item(self, item):
        raise NotImplementedError

    @abstractmethod
    def get_item(self):
        raise NotImplementedError

    @abstractmethod
    def has_waiting_client(self):
        raise NotImplementedError

    @abstractmethod
    def request_resource(self, item):
        raise NotImplementedError

    @abstractmethod
    def revoke_resource(self):
        raise NotImplementedError

    @abstractmethod
    def grant_resource(self):
        raise NotImplementedError


class Board(Resource):

    def __init__(self):
        self.in_use: bool = False
        self.queue = Queue()

    def insert_item(self, item):
        self.queue.put(item)

    def get_item(self):
        if self.queue.empty() is not True:
            return self.queue.get()

        return

    def has_waiting_client(self):
        return not self.queue.empty()

    def request_resource(self, item):
        if self.in_use:
            self.insert_item(item)
            return False
        else:
            self.in_use = True
            return True

    def revoke_resource(self):
        self.in_use = False

    def grant_resource(self):
        if self.has_waiting_client() and not self.in_use:
            if item := self.get_item():
                self.in_use = True
                return item

        return
