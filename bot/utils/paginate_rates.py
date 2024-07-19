import copy


class PaginateRates:
    def __init__(self) -> None:
        self._parts: list = list()
        self._part_index: int = -1

    def reset_all(self):
        self._part_index = -1
        self._total_count_of_rates = self._calculate_parts_length()
        self._part_last_index = self._total_count_of_rates - 1

    @property
    def current_rates(self):
        return self.rates

    @current_rates.setter
    def current_rates(self, rates: dict[str, dict]):
        self.rates = rates
        self._total_count_of_rates: int = self._calculate_parts_length()
        self._part_last_index = self._total_count_of_rates - 1

    def __len__(self):
        return len(self.rates)

    def __iter__(self):
        return self

    def __next__(self):
        self._part_index += 1
        return self._parts[self._part_index]

    def _calculate_parts_length(self) -> int:
        temp_part = list()
        parts = list()

        for index, currency_code in enumerate(self.rates, start=1):
            temp_part.append((self.rates[currency_code]["name"], index))

            if not index % 3:
                parts.append(copy.deepcopy(temp_part))
                temp_part.clear()

        parts.append(copy.deepcopy(temp_part))

        self._parts.clear()
        self._parts = parts

        return len(self._parts)


paginate_rates = PaginateRates()