"""
ساخت جدول عملکرد تک‌پارامتری.
Single Responsibility: فقط فرمت‌بندی جدول تک‌پارامتری.
"""

import pandas as pd
from typing import Dict

from .base_processor import BaseProcessor
from ..config import ScoringWeights


class SingleParamProcessor(BaseProcessor):

    def __init__(
        self,
        weights: ScoringWeights,
        scores: Dict[str, float],
        metrics: Dict[str, float],
    ):
        self._weights = weights
        self._scores = scores
        self._metrics = metrics

    def process(self) -> pd.DataFrame:
        w = self._weights.as_dict()
        rows = [
            {
                'پارامتر': 'نسبت تماس به فاکتور',
                'مقدار': f"{round(self._metrics['call_ratio'], 2)}%",
                'امتیاز (از 100)': round(self._scores['امتیاز نسبت تماس'], 2),
                'وزن': w['call_ratio'],
            },
            {
                'پارامتر': 'میانگین فاصله بین تماس',
                'مقدار': f"{round(self._metrics['avg_gap_seconds'], 1)} ثانیه",
                'امتیاز (از 100)': round(self._scores['امتیاز فاصله تماس'], 2),
                'وزن': w['avg_gap_seconds'],
            },
            {
                'پارامتر': 'نسبت فاکتور بدون تماس',
                'مقدار': f"{round(self._metrics['no_call_ratio'], 2)}%",
                'امتیاز (از 100)': round(self._scores['امتیاز فاکتور بدون تماس'], 2),
                'وزن': w['no_call_invoice_ratio'],
            },
            {
                'پارامتر': 'نسبت عدم پاسخگویی اپراتور',
                'مقدار': f"{round(self._metrics['op_no_answer_ratio'], 2)}%",
                'امتیاز (از 100)': round(self._scores['امتیاز عدم پاسخگویی اپراتور'], 2),
                'وزن': w['operator_no_answer_ratio'],
            },
            {
                'پارامتر': 'درصد پوشش تماس',
                'مقدار': f"{round(self._metrics['coverage_pct'], 2)}%",
                'امتیاز (از 100)': round(self._scores['امتیاز پوشش تماس'], 2),
                'وزن': w['call_coverage_pct'],
            },
            {
                'پارامتر': 'نسبت رد شده',
                'مقدار': f"{round(self._metrics['reject_ratio'], 2)}%",
                'امتیاز (از 100)': round(self._scores['امتیاز رد شده'], 2),
                'وزن': w['reject_ratio'],
            },
            {
                'پارامتر': 'نسبت تایید شده',
                'مقدار': f"{round(self._metrics['approve_ratio'], 2)}%",
                'امتیاز (از 100)': round(self._scores['امتیاز تایید شده'], 2),
                'وزن': w['approve_ratio'],
            },
        ]
        return pd.DataFrame(rows)
