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
    @abstractmethod
    def get_page_min_size():
        pass
