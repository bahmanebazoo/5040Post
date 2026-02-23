"""
اینترفیس پایه لودرها.
Interface Segregation + Dependency Inversion.
"""

from abc import ABC, abstractmethod


class BaseLoader(ABC):

    @abstractmethod
    def load(self):
        pass
