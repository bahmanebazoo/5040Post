# post_analyzer/processors/daily_processor.py

"""
پردازشگر محاسبات روزانه (گام‌های 1 تا 7).
Single Responsibility: فقط محاسبات سطح روز/اپراتور.
"""

import numpy as np
import pandas as pd
from datetime import timedelta
from typing import Dict, List, Optional, Tuple

from .base_processor import BaseProcessor
from ..config import AppConfig
from post_analyzer.models import (
    DailyRecord,
    GapStatistics,
    PanelColumns,
    PanelDayData,
    StatusCounts,
)
from ..utils.date_utils import JalaliDateUtils


class DailyProcessor(BaseProcessor):

    def __init__(
            self,
            config: AppConfig,
            df_call: pd.DataFrame,
            panel_data: Dict[str, Tuple[pd.DataFrame, PanelColumns]],
    ):
        self._config = config
        self._df_call = df_call
        self._panel_data = panel_data
        self._date_utils = JalaliDateUtils()

    def process(self) -> List[DailyRecord]:
        all_dates = sorted(
            self._df_call['تاریخ_شمسی_dash'].dropna().unique()
        )
        records: List[DailyRecord] = []

        for operator in self._config.target_operators:
            for date_dash in all_dates:
                date_slash = self._date_utils.dash_to_slash(date_dash)
                record = self._process_one_day(operator, date_dash, date_slash)
                if record is not None:
                    records.append(record)

        print(f"[DailyProcessor] تعداد رکوردهای روزانه: {len(records)}")
        return records

    # ----- private -----

    def _process_one_day(
            self, operator: str, date_dash: str, date_slash: str
    ) -> Optional[DailyRecord]:
        mask = (
                (self._df_call['تماس گیرنده'] == operator)
                & (self._df_call['تاریخ_شمسی'] == date_slash)
        )
        df_day = self._df_call[mask].copy()

        if len(df_day) == 0:
            return None

        df_day = df_day.sort_values('زمان_اعلام_dt').reset_index(drop=True)

        total_calls = len(df_day)
        unique_mobiles = df_day['موبایل'].nunique()
        status_counts = StatusCounts.from_series(df_day['وضعیت تماس'])
        gap_stats = self._compute_gaps(df_day)
        panel_day = self._get_panel_data(operator, date_dash)

        no_call_invoices = max(0, panel_day.total_review - unique_mobiles)

        # استخراج ساعت اولین تماس (کل تماس‌ها)
        first_call_time = self._get_first_call_time(df_day)

        # ✅ استخراج ساعت اولین تماس پاسخ داده شده
        first_answered_time = self._get_first_answered_time(df_day)

        return DailyRecord(
            operator=operator,
            date=date_slash,
            total_calls=total_calls,
            unique_mobiles=unique_mobiles,
            total_review=panel_day.total_review,
            no_call_invoices=no_call_invoices,
            gap_stats=gap_stats,
            status_counts=status_counts,
            approved_count=panel_day.approved_count,
            rejected_count=panel_day.rejected_count,
            first_call_time=first_call_time,
            first_answered_time=first_answered_time,
        )

    def _get_first_call_time(self, df_day: pd.DataFrame) -> str:
        """استخراج ساعت اولین تماس (هر وضعیتی)"""
        if df_day.empty:
            return "---"

        first_time = df_day.iloc[0]['زمان_اعلام_dt']

        if pd.isna(first_time):
            return "---"

        try:
            return first_time.strftime("%H:%M:%S")
        except Exception:
            return str(first_time)

    # ✅ متد جدید
    def _get_first_answered_time(self, df_day: pd.DataFrame) -> str:
        """
        استخراج ساعت اولین تماس با وضعیت "پاسخ داده شده".
        df_day قبلاً بر اساس زمان_اعلام_dt مرتب شده.

        Returns:
            str: ساعت به فرمت "HH:MM:SS" یا "---"
        """
        if df_day.empty:
            return "---"

        # فیلتر فقط تماس‌های پاسخ داده شده
        df_answered = df_day[df_day['وضعیت تماس'] == 'پاسخ داده']

        if df_answered.empty:
            return "---"

        # چون df_day قبلاً sort شده، اولین ردیف = زودترین تماس پاسخ داده
        first_time = df_answered.iloc[0]['زمان_اعلام_dt']

        if pd.isna(first_time):
            return "---"

        try:
            return first_time.strftime("%H:%M:%S")
        except Exception:
            return str(first_time)

    def _compute_gaps(self, df_day: pd.DataFrame) -> GapStatistics:
        """محاسبه فاصله بین تماس‌ها (گام 2)"""
        gaps: List[float] = []
        total_work = 0.0
        total_idle = 0.0

        for i in range(len(df_day)):
            row = df_day.iloc[i]
            status = row['وضعیت تماس']
            work_sec = self._config.status_config.get_work_seconds(status)
            total_work += work_sec

            if i < len(df_day) - 1:
                next_row = df_day.iloc[i + 1]

                end_time = row['زمان_پایان_dt']
                if pd.isna(end_time):
                    end_time = row['زمان_اعلام_dt']
                    if not pd.isna(end_time):
                        end_time = end_time + timedelta(seconds=work_sec)

                next_start = next_row['زمان_اعلام_dt']

                if not pd.isna(end_time) and not pd.isna(next_start):
                    gap = max(0.0, (next_start - end_time).total_seconds())
                    gaps.append(gap)
                    total_idle += gap

        return GapStatistics(
            avg_gap=float(np.mean(gaps)) if gaps else 0.0,
            median_gap=float(np.median(gaps)) if gaps else 0.0,
            max_gap=float(np.max(gaps)) if gaps else 0.0,
            min_gap=float(np.min(gaps)) if gaps else 0.0,
            total_idle_seconds=total_idle,
            total_work_seconds=total_work,
        )

    def _get_panel_data(self, operator: str, date_dash: str) -> PanelDayData:
        if date_dash not in self._panel_data:
            return PanelDayData()

        df_p, cols = self._panel_data[date_dash]

        if cols.operator is None:
            return PanelDayData()

        mask = df_p[cols.operator].astype(str).str.contains(operator, na=False)
        df_op = df_p[mask]

        if len(df_op) == 0:
            return PanelDayData()

        return PanelDayData(
            total_review=int(df_op[cols.total_review].sum()) if cols.total_review else 0,
            approved_count=int(df_op[cols.approved].sum()) if cols.approved else 0,
            rejected_count=int(df_op[cols.rejected].sum()) if cols.rejected else 0,
        )
