# post_analyzer/exporters/excel_exporter.py

"""
خروجی اکسل با استایل و نمودار.
"""

import pandas as pd
from typing import Dict, Optional
from openpyxl import Workbook

from .base_exporter import BaseExporter
from .excel_style import ExcelStyle


class ExcelExporter(BaseExporter):
    """ذخیره DataFrameها + استایل + نمودار"""

    TOTAL_ROW_SHEETS = {"عملکرد اپراتورها"}

    def __init__(self, output_file: str):
        self._output_file = output_file

    def export(
        self,
        sheets: Dict[str, pd.DataFrame],
        df_daily: Optional[pd.DataFrame] = None,
        df_operators: Optional[pd.DataFrame] = None,
    ) -> None:
        with pd.ExcelWriter(self._output_file, engine="openpyxl") as writer:
            # ── 1) نوشتن داده‌ها ──
            for sheet_name, df in sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

            # ── 2) اعمال استایل ──
            for sheet_name in list(writer.sheets.keys()):
                ws = writer.sheets[sheet_name]
                has_total = sheet_name in self.TOTAL_ROW_SHEETS
                ExcelStyle.apply_to_sheet(ws, has_total_row=has_total)
                print(f"  [Style] ✅ {sheet_name}")

            # ── 3) نمودارها ──
            if df_daily is not None and df_operators is not None:
                wb = writer.book
                print("\n[Charts] در حال ساخت نمودارها...")
                try:
                    from post_analyzer.charts import ChartManager

                    chart_manager = ChartManager(wb, df_daily, df_operators)
                    chart_manager.create_all_charts()
                except Exception as e:
                    print(f"  [Charts] ❌ خطا در ساخت نمودارها: {e}")
                    import traceback
                    traceback.print_exc()

        print(f"\n[ExcelExporter] ✅ فایل ذخیره شد: {self._output_file}")
