"""مدل شمارش وضعیت‌های تماس"""

from dataclasses import dataclass
import pandas as pd


@dataclass
class StatusCounts:
    answered: int = 0
    no_answer: int = 0
    operator_no_answer: int = 0
    busy: int = 0
    cancelled: int = 0

    @staticmethod
    def from_series(series: pd.Series) -> 'StatusCounts':
        counts = series.value_counts().to_dict()
        return StatusCounts(
            answered=counts.get('پاسخ داده', 0),
            no_answer=counts.get('عدم پاسخگویی', 0),
            operator_no_answer=counts.get('عدم پاسخگویی اپراتور', 0),
            busy=counts.get('مشغول بودن خط', 0),
            cancelled=counts.get('لغو تماس', 0),
        )
