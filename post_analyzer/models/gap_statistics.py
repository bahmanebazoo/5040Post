"""مدل آمار فاصله بین تماس‌ها"""

from dataclasses import dataclass


@dataclass
class GapStatistics:
    avg_gap: float = 0.0
    median_gap: float = 0.0
    max_gap: float = 0.0
    min_gap: float = 0.0
    total_idle_seconds: float = 0.0
    total_work_seconds: float = 0.0
