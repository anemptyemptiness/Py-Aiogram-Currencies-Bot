import copy
import xml.etree.ElementTree as ET
from inflection import underscore


class Parser:
    def __init__(
            self,
            xml_text: str,
    ) -> None:
        self._root: ET.XML = ET.fromstring(xml_text)
        self._data_dict: list[dict] = []

    def parse(self) -> list[dict[str, dict]]:
        for currency_data in self._root.findall("Valute"):
            dct: dict = dict()
            for data in currency_data:
                dct[underscore(data.tag)] = data.text
            self._data_dict.append(dct)

        self._data_dict = self._get_data_per_currency()

        return self._data_dict

    def _get_data_per_currency(self) -> list[dict[str, dict]]:
        list_of_currencies: list[dict] = list()
        temp_dct: dict[str, dict] = dict()

        for data in self._data_dict:
            temp_dct[data.pop("char_code")] = data
            list_of_currencies.append(copy.deepcopy(temp_dct))

            temp_dct.clear()

        return list_of_currencies
