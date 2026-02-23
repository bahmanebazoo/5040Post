"""اینترفیس پایه خروجی‌ها"""

from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd


class BaseExporter(ABC):

    @abstractmethod
    def export(self, sheets: Dict[str, pd.DataFrame]) -> None:
        pass
