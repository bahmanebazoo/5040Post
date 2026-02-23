"""
لودر شیت call.
Single Responsibility: فقط خواندن و آماده‌سازی دیتای تماس.
"""

import pandas as pd
from .base_loader import BaseLoader
from post_analyzer.config import AppConfig
from post_analyzer.utils.date_utils import JalaliDateUtils


class CallLoader(BaseLoader):

    def __init__(self, config: AppConfig):
        self._config = config
        self._date_utils = JalaliDateUtils()

    def load(self) -> pd.DataFrame:
        print("[CallLoader] در حال خواندن شیت call ...")
        df = pd.read_excel(
            self._config.input_file,
            sheet_name=self._config.call_sheet_name,
        )
        print(f"[CallLoader] تعداد کل رکوردها: {len(df)}")

        # فیلتر اپراتورهای هدف
        df = df[df['تماس گیرنده'].isin(self._config.target_operators)].copy()
        print(f"[CallLoader] رکوردهای اپراتورهای هدف: {len(df)}")

        # پردازش تاریخ
        df['زمان_اعلام_dt'] = df['زمان اعلام وضعیت'].apply(
            self._date_utils.parse_jalali_datetime
        )
        df['زمان_برقراری_dt'] = df['زمان برقراری تماس'].apply(
            self._date_utils.parse_jalali_datetime
        )
        df['زمان_پایان_dt'] = df['زمان پایان تماس'].apply(
            self._date_utils.parse_jalali_datetime
        )
        df['تاریخ_شمسی'] = df['زمان اعلام وضعیت'].apply(
            self._date_utils.extract_jalali_date
        )
        df['تاریخ_شمسی_dash'] = df['تاریخ_شمسی'].apply(
            self._date_utils.slash_to_dash
        )

        unique_dates = sorted(df['تاریخ_شمسی_dash'].dropna().unique())
        print(f"[CallLoader] تاریخ‌های یونیک: {unique_dates}")
        return df