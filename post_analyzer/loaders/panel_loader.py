"""
لودر شیت‌های پنل.
Single Responsibility: خواندن و شناسایی ستون‌های شیت‌های پنل.
"""

import pandas as pd
from typing import Dict, Tuple
from .base_loader import BaseLoader
from post_analyzer.config import AppConfig
from ..models.panel_columns import PanelColumns


class PanelLoader(BaseLoader):

    def __init__(self, config: AppConfig):
        self._config = config

    def load(self) -> Dict[str, Tuple[pd.DataFrame, PanelColumns]]:
        xls = pd.ExcelFile(self._config.input_file)
        panel_sheets = [
            s for s in xls.sheet_names
            if s != self._config.call_sheet_name
        ]
        print(f"[PanelLoader] شیت‌های پنل: {panel_sheets}")

        result = {}
        for sheet_name in panel_sheets:
            df = pd.read_excel(self._config.input_file, sheet_name=sheet_name)
            columns = self._detect_columns(df)
            result[sheet_name] = (df, columns)
            print(
                f"[PanelLoader] شیت {sheet_name}: {len(df)} رکورد | "
                f"اپراتور={columns.operator}, "
                f"کل_بررسی={columns.total_review}, "
                f"تایید={columns.approved}, "
                f"عدم_تایید={columns.rejected}"
            )
        return result

    def _detect_columns(self, df: pd.DataFrame) -> PanelColumns:
        """شناسایی هوشمند ستون‌های پنل"""
        cols = PanelColumns()
        col_names = list(df.columns)
        col_names_str = [str(c).strip() for c in col_names]

        for i, name in enumerate(col_names_str):
            if 'تعداد کل بررسی' in name or 'کل بررسی' in name:
                cols.total_review = col_names[i]
            if ('تعداد تایید' in name or name == 'تایید') and 'عدم' not in name:
                cols.approved = col_names[i]
            if 'عدم تایید' in name:
                cols.rejected = col_names[i]
            if 'نام' in name and ('کاربر' in name or 'اپراتور' in name):
                cols.operator = col_names[i]

        # فال‌بک: جستجو بر اساس محتوا
        if cols.operator is None:
            for i, c in enumerate(col_names):
                if df[c].dtype == 'object':
                    sample = df[c].dropna().head(10).tolist()
                    if any(
                        op in str(v)
                        for v in sample
                        for op in self._config.target_operators
                    ):
                        cols.operator = c
                        break

        if cols.operator is None and len(col_names) > 0:
            cols.operator = col_names[0]

        return cols
