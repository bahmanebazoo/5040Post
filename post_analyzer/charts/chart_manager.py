# post_analyzer/charts/chart_manager.py

"""
مدیر مرکزی ساخت تمام نمودارها.
"""

import pandas as pd
from openpyxl import Workbook

from .daily_calls_chart import DailyCallsChart
from .call_ratio_chart import CallRatioChart
from .gap_chart import GapChart
from .no_call_chart import NoCallChart
from .status_pie_chart import StatusPieChart
from .operator_score_chart import OperatorScoreChart
from .approve_reject_chart import ApproveRejectChart
from .coverage_chart import CoverageChart


class ChartManager:
    """
    هر نمودار را یکی‌یکی می‌سازد.
    اگر یکی خطا داد، بقیه ادامه پیدا می‌کنند.
    """

    def __init__(
        self,
        wb: Workbook,
        df_daily: pd.DataFrame,
        df_operators: pd.DataFrame,
    ):
        self._wb = wb
        self._df_daily = df_daily
        self._df_operators = df_operators

    def create_all_charts(self) -> None:
        chart_classes = [
            # نمودارهای مبتنی بر داده روزانه
            (DailyCallsChart,   self._df_daily),
            (CallRatioChart,    self._df_daily),
            (GapChart,          self._df_daily),
            (NoCallChart,       self._df_daily),
            # نمودارهای مبتنی بر عملکرد اپراتورها
            # (StatusPieChart,       self._df_operators),
            (OperatorScoreChart,   self._df_operators),
            (ApproveRejectChart,   self._df_operators),
            (CoverageChart,        self._df_operators),
        ]

        for chart_cls, df in chart_classes:
            name = chart_cls.__name__
            try:
                instance = chart_cls(self._wb, df)
                instance.create()
                print(f"  [Charts] ✅ {name}")
            except Exception as e:
                print(f"  [Charts] ❌ {name}: {e}")
                import traceback
                traceback.print_exc()
