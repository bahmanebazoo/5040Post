# post_analyzer/charts/call_ratio_chart.py

"""
نمودار ۲: نسبت تماس به فاکتور روزانه (Line Chart)
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference, Series

from .base_chart import BaseChart
from .chart_colors import get_color


class CallRatioChart(BaseChart):

    def __init__(self, wb: Workbook, df_daily: pd.DataFrame):
        super().__init__(wb, df_daily, sheet_prefix="نمودار_نسبت_تماس")

    def create(self) -> None:
        col_date = "تاریخ"
        col_operator = "اپراتور"
        col_ratio = "نسبت تماس به فاکتور (%)"

        if col_ratio not in self._df.columns:
            print(f"  [CallRatioChart] ⚠ ستون '{col_ratio}' یافت نشد.")
            return

        pivot = self._df.pivot_table(
            index=col_date, columns=col_operator, values=col_ratio,
            aggfunc="mean", fill_value=0
        )
        pivot = pivot.reset_index()
        self._write_data_sheet(pivot)

        ws = self._get_data_sheet()
        max_row = ws.max_row
        max_col = ws.max_column

        chart = LineChart()
        self._apply_common_settings(chart, "نسبت تماس به فاکتور (%) — روزانه")

        cats = self._make_cat_ref(ws, col=1, min_row=2, max_row=max_row)

        for idx, col_idx in enumerate(range(2, max_col + 1)):
            ref = Reference(ws, min_col=col_idx, min_row=1, max_row=max_row)
            series = Series(ref, title_from_data=True)
            series.graphicalProperties.line.solidFill = get_color(idx)
            series.smooth = True
            chart.series.append(series)

        chart.set_categories(cats)
        self._set_axis_labels(chart, x_title="تاریخ", y_title="درصد (%)")
        self._place_chart(chart)
