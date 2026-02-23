"""مدل نگهداری نام ستون‌های شناسایی‌شده در شیت پنل"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PanelColumns:
    operator: Optional[str] = None
    total_review: Optional[str] = None
    approved: Optional[str] = None
    rejected: Optional[str] = None
