"""مدل داده‌های پنل برای یک اپراتور در یک روز"""

from dataclasses import dataclass


@dataclass
class PanelDayData:
    total_review: int = 0
    approved_count: int = 0
    rejected_count: int = 0
