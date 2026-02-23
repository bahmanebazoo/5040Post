"""
ابزارهای تاریخ شمسی (جلالی).
Single Responsibility: فقط مسئول تبدیل و پردازش تاریخ.
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


class JalaliDateUtils:

    @staticmethod
    def parse_jalali_datetime(dt_str) -> Optional[datetime]:
        """
        تبدیل رشته تاریخ شمسی yyyy/MM/dd hh:mm:ss
        به datetime ساختگی برای محاسبه فاصله زمانی.
        """
        if pd.isna(dt_str) or str(dt_str).strip() == '':
            return pd.NaT
        try:
            dt_str = str(dt_str).strip()
            parts = dt_str.split(' ')
            date_part = parts[0]
            time_part = parts[1] if len(parts) > 1 else '00:00:00'

            y, m, d = map(int, date_part.split('/'))
            h, mi, s = map(int, time_part.split(':'))

            base = datetime(2000, 1, 1)
            total_days = (y - 1400) * 365 + (m - 1) * 30 + d
            return base + timedelta(days=total_days, hours=h, minutes=mi, seconds=s)
        except Exception:
            return pd.NaT

    @staticmethod
    def extract_jalali_date(dt_str) -> Optional[str]:
        """استخراج بخش تاریخ از رشته datetime شمسی -> yyyy/MM/dd"""
        if pd.isna(dt_str) or str(dt_str).strip() == '':
            return None
        try:
            return str(dt_str).strip().split(' ')[0]
        except Exception:
            return None

    @staticmethod
    def slash_to_dash(date_str: str) -> Optional[str]:
        """تبدیل yyyy/MM/dd به yyyy-MM-dd"""
        if date_str is None:
            return None
        return date_str.replace('/', '-')

    @staticmethod
    def dash_to_slash(date_str: str) -> Optional[str]:
        """تبدیل yyyy-MM-dd به yyyy/MM/dd"""
        if date_str is None:
            return None
        return date_str.replace('-', '/')
