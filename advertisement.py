from dataclasses import dataclass
from datetime import datetime
import json


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


def adv_to_tuple(adv: Advertisement):
    return (adv.title, adv.website, adv.price,
            adv.link, adv.size, adv.floor,
            json.dumps(adv.metadata, indent=4), adv.dt, adv.search_name)


def tuple_to_adv(adv: tuple):
    title, website, price, link, size, floor, metadata_str, dt_str, search_name = adv
    return Advertisement(title, website, price, link,
                         size, floor, json.loads(metadata_str),
                         datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f'), search_name)
