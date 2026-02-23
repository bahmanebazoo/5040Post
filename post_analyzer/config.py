"""
تنظیمات مرکزی برنامه.
برای تغییر رفتار برنامه فقط این فایل رو ویرایش کنید.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class StatusWorkConfig:
    """
    مدت کارکرد (ثانیه) به ازای هر وضعیت تماس.
    برای اضافه کردن وضعیت جدید، فقط یک آیتم به دیکشنری اضافه کنید.
    """
    status_seconds: Dict[str, int] = field(default_factory=lambda: {
        'پاسخ داده': 60,
        'عدم پاسخگویی': 60,
        'عدم پاسخگویی اپراتور': 60,
        'مشغول بودن خط': 60,
        'لغو تماس': 60,
    })
    default_seconds: int = 60

    def get_work_seconds(self, status: str) -> int:
        return self.status_seconds.get(status, self.default_seconds)


@dataclass
class ScoringWeights:
    """
    وزن‌های امتیازدهی.
    مقدار پیش‌فرض = 1 برای همه. قابل اپتیمایز.
    """
    call_ratio: float = 1.0
    avg_gap_seconds: float = 1.0
    no_call_invoice_ratio: float = 1.0
    operator_no_answer_ratio: float = 1.0
    call_coverage_pct: float = 1.0
    reject_ratio: float = 1.0
    approve_ratio: float = 1.0

    def as_dict(self) -> Dict[str, float]:
        return {
            'call_ratio': self.call_ratio,
            'avg_gap_seconds': self.avg_gap_seconds,
            'no_call_invoice_ratio': self.no_call_invoice_ratio,
            'operator_no_answer_ratio': self.operator_no_answer_ratio,
            'call_coverage_pct': self.call_coverage_pct,
            'reject_ratio': self.reject_ratio,
            'approve_ratio': self.approve_ratio,
        }

    def total_weight(self) -> float:
        return sum(self.as_dict().values())


@dataclass
class AppConfig:
    """تنظیمات اصلی برنامه"""
    input_file: str = '../post.xlsx'
    output_file: str = '../post_report.xlsx'
    target_operators: List[str] = field(default_factory=lambda: [
        'زهرا فرشباف',
        'افشین دلبسته',
        'افسانه جوادی',
        'افسانه عسکری بقرآبادی',
        'حانیه اکبری',
    ])
    status_config: StatusWorkConfig = field(default_factory=StatusWorkConfig)
    scoring_weights: ScoringWeights = field(default_factory=ScoringWeights)
    call_sheet_name: str = 'call'
