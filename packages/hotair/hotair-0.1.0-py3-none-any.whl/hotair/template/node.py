import abc


class Node(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def serialised(self) -> str:
        raise NotImplementedError

    def render(self):
        return self
