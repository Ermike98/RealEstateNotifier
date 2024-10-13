from search import Search
from advertisement import Advertisement
from datetime import datetime
import time
from bs4 import BeautifulSoup



def floor_str_to_num(floor_str: str) -> float:
    floor_str = floor_str.lower()
    if floor_str == "t" or floor_str == "r":
        return 0.

    try:
        return float(floor_str)
    except ValueError as e:
        return -1.


def metadata_list_to_dict(l: list) -> dict:
    d = dict()
    for el in l:
        el_str = el.lower()
        if "m²" in el_str:
            d["size"] = el
        elif "local" in el_str:
            d["locali"] = el
        elif "bagn" in el_str:
            d["bagni"] = el
        elif "piano" in el_str:
            d["piano"] = el
        else:
            d[el.lower().replace(" ", "_")] = el

    try:
        if "size" in d:
            d["size_num"] = float(d["size"].split(" ")[0])
        else:
            d["size_num"] = 0
    except ValueError as e:
        d["size_num"] = 0

    try:
        if "locali" in d:
            d["locali_num"] = float(d["locali"].split(" ")[0])
        else:
            d["locali_num"] = 0
    except ValueError as e:
        d["locali_num"] = 0

    try:
        if "bagni" in d:
            d["bagni_num"] = float(d["bagni"].split(" ")[0])
        else:
            d["bagni_num"] = 0
    except ValueError as e:
        d["bagni_num"] = 0

    if "piano" in d:
        d["piano_num"] = floor_str_to_num(d["piano"].split(" ")[1])
    else:
        d["piano_num"] = 0
    return d


class ImmobiliareSearch(Search):
    def __init__(self, driver, search_name, search_link):
        self.__driver = driver
        self.__search_name = search_name
        self.__search_link = search_link

    def __parse_adv(self, adv_soup) -> Advertisement:
        adv_info_soup = adv_soup.find("div", "nd-mediaObject__content in-listingCardPropertyContent")

        price_str = adv_info_soup.find("div", "in-listingCardPrice").string
        adv_price = float(price_str.split()[1].split("/")[0].replace(".", ""))

        card_title = adv_info_soup.find("a", "in-listingCardTitle")
        adv_link = card_title["href"]
        adv_title = card_title.string

        adv_features_soup = adv_info_soup.find("div", "in-listingCardFeatureList has-lowVisibility")
        if adv_features_soup is not None:
            metadata_str_list = list(map(lambda x: x.string, adv_features_soup.find_all("span")))
        else:
            metadata_str_list = []

        adv_metadata = metadata_list_to_dict(metadata_str_list)

        return Advertisement(adv_title, "Immobiliare", adv_price, adv_link,
                             adv_metadata["size_num"], adv_metadata["piano_num"], adv_metadata,
                             datetime.now(), self.__search_name)

    def search(self) -> list[Advertisement]:
        self.__driver.get(self.__search_link)
        time.sleep(0.5)
        content = self.__driver.page_source

        # with open("test_immo.html", "w", encoding="utf-8") as f:
        #     f.write(content)

        soup = BeautifulSoup(content, 'html.parser')
        advs_soup = soup.find_all("li", "nd-list__item in-searchLayoutListItem")
        return list(map(self.__parse_adv, advs_soup))
