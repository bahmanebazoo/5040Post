"""
خروجی اکسل.
Single Responsibility: فقط مسئول ذخیره DataFrameها در فایل اکسل.
"""

import pandas as pd
from typing import Dict
from .base_exporter import BaseExporter


class ExcelExporter(BaseExporter):

    def __init__(self, output_file: str):
        self._output_file = output_file

    def export(self, sheets: Dict[str, pd.DataFrame]) -> None:
        with pd.ExcelWriter(self._output_file, engine='openpyxl') as writer:
            for sheet_name, df in sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

            # تنظیم عرض ستون‌ها
            for sheet_name in writer.sheets:
                ws = writer.sheets[sheet_name]
                for column in ws.columns:
                    max_len = 0
                    col_letter = column[0].column_letter
                    for cell in column:
                        try:
                            cell_len = len(str(cell.value))
                            if cell_len > max_len:
                                max_len = cell_len
                        except Exception:
                            pass
                    ws.column_dimensions[col_letter].width = min(max_len + 4, 50)

        print(f"[ExcelExporter] فایل ذخیره شد: {self._output_file}")
