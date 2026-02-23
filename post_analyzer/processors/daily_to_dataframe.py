"""
تبدیل لیست DailyRecord به DataFrame خروجی.
Single Responsibility: فقط مسئول تبدیل فرمت.
"""

import pandas as pd
from typing import List
from post_analyzer.models import DailyRecord


class DailyToDataFrame:

    @staticmethod
    def convert(records: List[DailyRecord]) -> pd.DataFrame:
        rows = []
        for r in records:
            rows.append({
                'اپراتور': r.operator,
                'تاریخ': r.date,
                'تعداد کل تماس': r.total_calls,
                'تعداد شماره یونیک تماس': r.unique_mobiles,
                'تعداد کل بررسی (پنل)': r.total_review,
                'نسبت تماس به فاکتور (%)': round(r.call_to_invoice_ratio, 2),
                'تعداد فاکتور بدون تماس': r.no_call_invoices,
                'نسبت فاکتور بدون تماس (%)': round(r.no_call_ratio, 2),
                'میانگین فاصله بین تماس (ثانیه)': round(r.gap_stats.avg_gap, 1),
                'میانه فاصله بین تماس (ثانیه)': round(r.gap_stats.median_gap, 1),
                'حداکثر فاصله بین تماس (ثانیه)': round(r.gap_stats.max_gap, 1),
                'حداقل فاصله بین تماس (ثانیه)': round(r.gap_stats.min_gap, 1),
                'کل زمان کارکرد (ثانیه)': round(r.gap_stats.total_work_seconds, 1),
                'کل زمان بیکاری (ثانیه)': round(r.gap_stats.total_idle_seconds, 1),
                'تعداد پاسخ داده': r.status_counts.answered,
                'تعداد عدم پاسخگویی': r.status_counts.no_answer,
                'تعداد عدم پاسخگویی اپراتور': r.status_counts.operator_no_answer,
                'تعداد مشغول بودن خط': r.status_counts.busy,
                'تعداد لغو تماس': r.status_counts.cancelled,
                'درصد تماس پست (%)': round(r.call_coverage_pct, 2),
                'تعداد تایید شده': r.approved_count,
                'تعداد رد شده (عدم تایید)': r.rejected_count,
                'نسبت تایید (%)': round(r.approve_ratio, 2),
                'نسبت رد (%)': round(r.reject_ratio, 2),
            })
        return pd.DataFrame(rows)
