from abc import ABC, abstractmethod


# interface for pages
class Page(ABC):
    # title of page
    @staticmethod
    @abstractmethod
    def get_page_title():
        pass

    # size on load
    @staticmethod
    @abstractmethod
    def get_page_size():
        pass

    # minimum size
    @staticmethod
    def get_page_min_size():
        return "10x10"

    # minimum size
    # returns None if there is no limit
    @staticmethod
    def get_page_max_size():
        return None
