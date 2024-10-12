from abc import ABC, abstractmethod
from advertisement import Advertisement


class Search(ABC):
    @abstractmethod
    def search(self) -> list[Advertisement]:
        pass
