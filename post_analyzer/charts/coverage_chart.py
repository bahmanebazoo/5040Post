# post_analyzer/charts/coverage_chart.py

"""
نمودار ۸: درصد پوشش تماس اپراتورها (Bar Chart)
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.chart.series import DataPoint

from .base_chart import BaseChart
from .chart_colors import get_color, TOTAL_COLOR


class CoverageChart(BaseChart):

    def __init__(self, wb: Workbook, df_operators: pd.DataFrame):
        super().__init__(wb, df_operators, sheet_prefix="نمودار_پوشش_تماس")

    def create(self) -> None:
        col_op = "اپراتور"
        col_cov = "درصد تماس پست (%)"

        if col_cov not in self._df.columns:
            print(f"  [CoverageChart] ⚠ ستون '{col_cov}' یافت نشد.")
            return

        df_sub = self._df[[col_op, col_cov]].copy()
        self._write_data_sheet(df_sub)

        ws = self._get_data_sheet()
        max_row = ws.max_row

        chart = BarChart()
        chart.grouping = "clustered"
        self._apply_common_settings(chart, "درصد پوشش تماس اپراتورها")

        cats = Reference(ws, min_col=1, min_row=2, max_row=max_row)
        data = Reference(ws, min_col=2, min_row=1, max_row=max_row)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        chart.legend = None

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
        self._set_axis_labels(chart, x_title="اپراتور", y_title="درصد (%)")
        self._place_chart(chart)
