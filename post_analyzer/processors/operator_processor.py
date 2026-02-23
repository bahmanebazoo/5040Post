"""
تجمیع عملکرد اپراتورها + سطر جمع کل پست (گام 8 و 9).
Single Responsibility: فقط تجمیع و امتیازدهی سطح اپراتور.
"""

import numpy as np
import pandas as pd
from typing import Dict, List

from .base_processor import BaseProcessor
from .scoring import Scorer
from ..config import AppConfig
from post_analyzer.models import DailyRecord


class OperatorProcessor(BaseProcessor):

    def __init__(
        self,
        config: AppConfig,
        daily_records: List[DailyRecord],
        scorer: Scorer,
    ):
        self._config = config
        self._daily_records = daily_records
        self._scorer = scorer

    def process(self) -> pd.DataFrame:
        """
        خروجی: DataFrame شامل یک سطر هر اپراتور + یک سطر «جمع کل پست».
        """
        rows: List[Dict] = []

        for operator in self._config.target_operators:
            op_records = [
                r for r in self._daily_records if r.operator == operator
            ]
            if not op_records:
                continue
            rows.append(self._aggregate(operator, op_records))

        # سطر تجمیعی
        if self._daily_records:
            rows.append(self._aggregate('جمع کل پست', self._daily_records))

        df = pd.DataFrame(rows)
        print(f"[OperatorProcessor] تعداد سطرها (شامل جمع کل): {len(df)}")
        return df

    # ----- private -----

    def _aggregate(self, label: str, records: List[DailyRecord]) -> Dict:
        total_calls = sum(r.total_calls for r in records)
        total_unique = sum(r.unique_mobiles for r in records)
        total_review = sum(r.total_review for r in records)
        total_no_call = sum(r.no_call_invoices for r in records)
        total_op_no_ans = sum(r.status_counts.operator_no_answer for r in records)
        total_approved = sum(r.approved_count for r in records)
        total_rejected = sum(r.rejected_count for r in records)
        total_answered = sum(r.status_counts.answered for r in records)
        total_no_answer = sum(r.status_counts.no_answer for r in records)
        total_busy = sum(r.status_counts.busy for r in records)
        total_cancelled = sum(r.status_counts.cancelled for r in records)
        total_work_sec = sum(r.gap_stats.total_work_seconds for r in records)
        total_idle_sec = sum(r.gap_stats.total_idle_seconds for r in records)

        avg_gaps = [r.gap_stats.avg_gap for r in records if r.gap_stats.avg_gap > 0]
        avg_gap_overall = float(np.mean(avg_gaps)) if avg_gaps else 0.0

        call_ratio = (total_unique / total_review * 100) if total_review > 0 else 0
        no_call_ratio = (total_no_call / total_review * 100) if total_review > 0 else 0
        op_no_ans_ratio = (total_op_no_ans / total_calls * 100) if total_calls > 0 else 0
        coverage_pct = (total_unique / total_review * 100) if total_review > 0 else 0
        approve_ratio = (total_approved / total_review * 100) if total_review > 0 else 0
        reject_ratio = (total_rejected / total_review * 100) if total_review > 0 else 0

        metrics = {
            'call_ratio': call_ratio,
            'avg_gap_seconds': avg_gap_overall,
            'no_call_ratio': no_call_ratio,
            'op_no_answer_ratio': op_no_ans_ratio,
            'coverage_pct': coverage_pct,
            'reject_ratio': reject_ratio,
            'approve_ratio': approve_ratio,
        }

        scores = self._scorer.compute_scores(metrics)
        overall = self._scorer.compute_overall(scores)

        return {
            'اپراتور': label,
            'تعداد روز فعال': len(set(r.date for r in records)),
            'تعداد کل تماس': total_calls,
            'تعداد شماره یونیک تماس': total_unique,
            'تعداد کل بررسی (پنل)': total_review,
            'نسبت تماس به فاکتور (%)': round(call_ratio, 2),
            'میانگین فاصله بین تماس (ثانیه)': round(avg_gap_overall, 1),
            'تعداد فاکتور بدون تماس': total_no_call,
            'نسبت فاکتور بدون تماس (%)': round(no_call_ratio, 2),
            'تعداد پاسخ داده': total_answered,
            'تعداد عدم پاسخگویی': total_no_answer,
            'تعداد عدم پاسخگویی اپراتور': total_op_no_ans,
            'نسبت عدم پاسخگویی اپراتور (%)': round(op_no_ans_ratio, 2),
            'تعداد مشغول بودن خط': total_busy,
            'تعداد لغو تماس': total_cancelled,
            'درصد تماس پست (%)': round(coverage_pct, 2),
            'تعداد تایید شده': total_approved,
            'تعداد رد شده': total_rejected,
            'نسبت تایید (%)': round(approve_ratio, 2),
            'نسبت رد (%)': round(reject_ratio, 2),
            'کل زمان کارکرد (ثانیه)': round(total_work_sec, 1),
            'کل زمان بیکاری (ثانیه)': round(total_idle_sec, 1),
            **{k: round(v, 2) for k, v in scores.items()},
            'امتیاز کلی عملکرد': round(overall, 2),
        }
