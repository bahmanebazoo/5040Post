# post_analyzer/charts/approve_reject_chart.py

"""
نمودار ۷: نسبت تایید و رد هر اپراتور (Grouped Bar)
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference, Series

from .base_chart import BaseChart


class ApproveRejectChart(BaseChart):

    def __init__(self, wb: Workbook, df_operators: pd.DataFrame):
        super().__init__(wb, df_operators, sheet_prefix="نمودار_تایید_رد")

    def create(self) -> None:
        col_op = "اپراتور"
        col_approve = "نسبت تایید (%)"
        col_reject = "نسبت رد (%)"

        needed = [col_op, col_approve, col_reject]
        for c in needed:
            if c not in self._df.columns:
                print(f"  [ApproveRejectChart] ⚠ ستون '{c}' یافت نشد.")
                return

        # حذف سطر جمع کل برای مقایسه بهتر
        df_sub = self._df[self._df[col_op] != "جمع کل پست"][needed].copy()
        if df_sub.empty:
            return

        self._write_data_sheet(df_sub)

        ws = self._get_data_sheet()
        max_row = ws.max_row

        chart = BarChart()
        chart.grouping = "clustered"
        self._apply_common_settings(chart, "مقایسه نسبت تایید و رد اپراتورها")

        cats = Reference(ws, min_col=1, min_row=2, max_row=max_row)

        # ستون تایید (col=2)
        ref_approve = Reference(ws, min_col=2, min_row=1, max_row=max_row)
        s_approve = Series(ref_approve, title_from_data=True)
        s_approve.graphicalProperties.solidFill = "70AD47"  # سبز
        chart.series.append(s_approve)

        # ستون رد (col=3)
        ref_reject = Reference(ws, min_col=3, min_row=1, max_row=max_row)
        s_reject = Series(ref_reject, title_from_data=True)
        s_reject.graphicalProperties.solidFill = "ED7D31"  # نارنجی
        chart.series.append(s_reject)

        chart.set_categories(cats)
        self._set_axis_labels(chart, x_title="اپراتور", y_title="درصد (%)")
        self._enable_data_labels(chart)
        self._place_chart(chart)
