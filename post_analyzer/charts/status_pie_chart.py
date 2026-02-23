# post_analyzer/charts/status_pie_chart.py

"""
نمودار ۵: وضعیت تماس‌ها — کل دوره (Pie Chart)
بر اساس df_operators (سطر جمع کل)
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import PieChart, Reference, Series
from openpyxl.chart.label import DataLabelList

from .base_chart import BaseChart


class StatusPieChart(BaseChart):

    def __init__(self, wb: Workbook, df_operators: pd.DataFrame):
        super().__init__(wb, df_operators, sheet_prefix="نمودار_وضعیت_تماس")

    def create(self) -> None:
        # پیدا کردن سطر "جمع کل پست"
        total = self._df[self._df["اپراتور"] == "جمع کل پست"]
        if total.empty:
            print("  [StatusPieChart] ⚠ سطر 'جمع کل پست' یافت نشد.")
            return

        tr = total.iloc[0]

        # ستون‌های مربوط به وضعیت تماس
        status_cols = {
            "پاسخ داده": "تعداد پاسخ‌داده",
            "بی‌پاسخ": "تعداد بی‌پاسخ",
            "رد شده": "تعداد رد شده",
            "مسدود": "تعداد مسدود",
        }

        labels = []
        values = []
        for label, col_name in status_cols.items():
            if col_name in tr.index:
                val = tr[col_name]
                if pd.notna(val) and val > 0:
                    labels.append(label)
                    values.append(int(val))

        if not values:
            print("  [StatusPieChart] ⚠ داده‌ای برای Pie Chart یافت نشد.")
            return

        # ساخت شیت داده کمکی
        df_pie = pd.DataFrame({"وضعیت": labels, "تعداد": values})
        self._write_data_sheet(df_pie)

        ws = self._get_data_sheet()
        max_row = ws.max_row

        chart = PieChart()
        chart.title = "وضعیت کل تماس‌ها"
        chart.width = self.DEFAULT_WIDTH
        chart.height = self.DEFAULT_HEIGHT
        chart.style = 10

        cats = Reference(ws, min_col=1, min_row=2, max_row=max_row)
        data = Reference(ws, min_col=2, min_row=1, max_row=max_row)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)

        # رنگ‌های ثابت وضعیت‌ها
        pie_colors = ["70AD47", "FFC000", "ED7D31", "A5A5A5"]
        from openpyxl.chart.series import DataPoint
        from openpyxl.drawing.fill import PatternFillProperties, ColorChoice

        for i, color in enumerate(pie_colors[:len(values)]):
            pt = DataPoint(idx=i)
            pt.graphicalProperties.solidFill = color
            chart.series[0].data_points.append(pt)

        # برچسب داده‌ها
        chart.series[0].dLbls = DataLabelList()
        chart.series[0].dLbls.showPercent = True
        chart.series[0].dLbls.showVal = True
        chart.series[0].dLbls.showCatName = True

        # لجند
        chart.legend.position = "r"

        self._place_chart(chart)
