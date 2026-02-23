# post_analyzer/models/daily_record.py

"""مدل رکورد روزانه عملکرد یک اپراتور"""

from dataclasses import dataclass
from typing import Optional
from .gap_statistics import GapStatistics
from .status_counts import StatusCounts


@dataclass
class DailyRecord:
    operator: str
    date: str
    total_calls: int
    unique_mobiles: int
    total_review: int
    no_call_invoices: int
    gap_stats: GapStatistics
    status_counts: StatusCounts
    approved_count: int
    rejected_count: int
    first_call_time: Optional[str] = None    # ✅ ساعت اولین تماس
    first_answered_time: Optional[str] = None    # ✅ ساعت اولین تماس پاسخ داده

    @property
    def call_to_invoice_ratio(self) -> float:
        return (self.unique_mobiles / self.total_review * 100) if self.total_review > 0 else 0

    @property
    def no_call_ratio(self) -> float:
        return (self.no_call_invoices / self.total_review * 100) if self.total_review > 0 else 0

    @property
    def call_coverage_pct(self) -> float:
        return (self.unique_mobiles / self.total_review * 100) if self.total_review > 0 else 0

    @property
    def approve_ratio(self) -> float:
        return (self.approved_count / self.total_review * 100) if self.total_review > 0 else 0

    @property
    def reject_ratio(self) -> float:
        return (self.rejected_count / self.total_review * 100) if self.total_review > 0 else 0
