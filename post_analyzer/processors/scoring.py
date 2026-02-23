"""
موتور امتیازدهی.
Single Responsibility: فقط محاسبه امتیاز.
Open/Closed: با تغییر وزن‌ها قابل تنظیم بدون تغییر کد.
"""

from typing import Dict
from ..config import ScoringWeights


class Scorer:

    # نگاشت کلید وزن -> کلید امتیاز فارسی
    _SCORE_KEY_MAP = {
        'call_ratio': 'امتیاز نسبت تماس',
        'avg_gap_seconds': 'امتیاز فاصله تماس',
        'no_call_invoice_ratio': 'امتیاز فاکتور بدون تماس',
        'operator_no_answer_ratio': 'امتیاز عدم پاسخگویی اپراتور',
        'call_coverage_pct': 'امتیاز پوشش تماس',
        'reject_ratio': 'امتیاز رد شده',
        'approve_ratio': 'امتیاز تایید شده',
    }

    def __init__(self, weights: ScoringWeights):
        self._weights = weights

    def compute_scores(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """
        محاسبه امتیاز هر شاخص (0-100).
        metrics keys: call_ratio, avg_gap_seconds, no_call_ratio,
                      op_no_answer_ratio, coverage_pct, reject_ratio, approve_ratio
        """
        return {
            'امتیاز نسبت تماس': min(metrics.get('call_ratio', 0), 100),
            'امتیاز فاصله تماس': max(0, 100 - (metrics.get('avg_gap_seconds', 0) / 60)),
            'امتیاز فاکتور بدون تماس': max(0, 100 - metrics.get('no_call_ratio', 0)),
            'امتیاز عدم پاسخگویی اپراتور': max(0, 100 - metrics.get('op_no_answer_ratio', 0)),
            'امتیاز پوشش تماس': min(metrics.get('coverage_pct', 0), 100),
            'امتیاز رد شده': max(0, 100 - metrics.get('reject_ratio', 0)),
            'امتیاز تایید شده': min(metrics.get('approve_ratio', 0), 100),
        }

    def compute_overall(self, scores: Dict[str, float]) -> float:
        """محاسبه امتیاز کلی با میانگین وزن‌دار"""
        w = self._weights.as_dict()
        total = sum(
            w[weight_key] * scores[self._SCORE_KEY_MAP[weight_key]]
            for weight_key in w
        )
        return total / self._weights.total_weight()
