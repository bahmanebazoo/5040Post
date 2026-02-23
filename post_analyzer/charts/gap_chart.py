# post_analyzer/charts/gap_chart.py

"""
نمودار ۳: میانگین فاصله بین تماس — روزانه (Bar Chart)
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference, Series

from .base_chart import BaseChart
from .chart_colors import get_color


class GapChart(BaseChart):

    def __init__(self, wb: Workbook, df_daily: pd.DataFrame):
        super().__init__(wb, df_daily, sheet_prefix="نمودار_فاصله_تماس")

    def create(self) -> None:
        col_date = "تاریخ"
        col_operator = "اپراتور"
        col_gap = "میانگین فاصله بین تماس (ثانیه)"

        if col_gap not in self._df.columns:
            print(f"  [GapChart] ⚠ ستون '{col_gap}' یافت نشد.")
            return

        pivot = self._df.pivot_table(
            index=col_date, columns=col_operator, values=col_gap,
            aggfunc="mean", fill_value=0
        )
        pivot = pivot.reset_index()
        self._write_data_sheet(pivot)

        ws = self._get_data_sheet()
        max_row = ws.max_row
        max_col = ws.max_column

        chart = BarChart()
        chart.grouping = "clustered"
        self._apply_common_settings(chart, "میانگین فاصله بین تماس (ثانیه) — روزانه")

        cats = self._make_cat_ref(ws, col=1, min_row=2, max_row=max_row)

        for idx, col_idx in enumerate(range(2, max_col + 1)):
            ref = Reference(ws, min_col=col_idx, min_row=1, max_row=max_row)
            series = Series(ref, title_from_data=True)
            series.graphicalProperties.solidFill = get_color(idx)
            chart.series.append(series)

        chart.set_categories(cats)
        self._set_axis_labels(chart, x_title="تاریخ", y_title="ثانیه")
        # self._enable_data_labels(chart)
        self._place_chart(chart)
