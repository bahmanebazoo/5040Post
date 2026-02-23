# post_analyzer/charts/operator_score_chart.py

"""
نمودار ۶: امتیاز کلی عملکرد اپراتورها (Horizontal Bar)
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.chart.series import DataPoint

from .base_chart import BaseChart
from .chart_colors import get_color, TOTAL_COLOR


class OperatorScoreChart(BaseChart):

    def __init__(self, wb: Workbook, df_operators: pd.DataFrame):
        super().__init__(wb, df_operators, sheet_prefix="نمودار_امتیاز_اپراتور")

    def create(self) -> None:
        col_op = "اپراتور"
        col_score = "امتیاز کلی عملکرد"

        if col_score not in self._df.columns:
            print(f"  [OperatorScoreChart] ⚠ ستون '{col_score}' یافت نشد.")
            return

        df_sub = self._df[[col_op, col_score]].copy()
        self._write_data_sheet(df_sub)

        ws = self._get_data_sheet()
        max_row = ws.max_row

        chart = BarChart()
        chart.type = "bar"  # horizontal
        chart.grouping = "clustered"
        self._apply_common_settings(chart, "امتیاز کلی عملکرد اپراتورها")

        cats = Reference(ws, min_col=1, min_row=2, max_row=max_row)
        data = Reference(ws, min_col=2, min_row=1, max_row=max_row)

        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        chart.legend = None  # نیازی به لجند نیست

        # رنگ هر ستون
        for i in range(max_row - 1):
            op_name = ws.cell(row=i + 2, column=1).value
            pt = DataPoint(idx=i)
            if op_name == "جمع کل پست":
                pt.graphicalProperties.solidFill = TOTAL_COLOR
            else:
                pt.graphicalProperties.solidFill = get_color(i)
            chart.series[0].data_points.append(pt)

        self._enable_data_labels(chart)
        self._set_axis_labels(chart, x_title="امتیاز", y_title="اپراتور")
        self._place_chart(chart)
