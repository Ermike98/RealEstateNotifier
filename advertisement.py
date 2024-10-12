from dataclasses import dataclass
from datetime import datetime


@dataclass
class Advertisement:
    title: str
    website: str
    price: float
    link: str
    size: float
    floor: float
    metadata: dict
    dt: datetime
    search_name: str

    def __eq__(self, other):
        return self.link == other.link
