import math


class Paginator:
    def __init__(self, array, page: int = 1, per_page: int = 1):
        self.array = array
        self.per_page = per_page
        self.page = page
        self.len = len(self.array)
        self.pages = math.ceil(self.len / self.per_page)

    def __get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self):
        return self.__get_slice()

    def has_next(self):
        return self.page < self.pages

    def has_previous(self):
        return self.page > 1
