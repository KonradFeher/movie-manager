from abc import ABC, abstractmethod


class Page(ABC):
    @staticmethod
    @abstractmethod
    def get_page_title():
        pass

    @staticmethod
    @abstractmethod
    def get_page_size():
        pass

    @staticmethod
    def get_page_min_size():
        return "10x10"

    # returns False if there is no limit
    @staticmethod
    def get_page_max_size():
        return None
