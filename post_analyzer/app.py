# post_analyzer/app.py

"""
هماهنگ‌کننده اصلی (Orchestrator).
"""

import pandas as pd

from post_analyzer.config import AppConfig
from post_analyzer.loaders import CallLoader, PanelLoader
from post_analyzer.processors import (
    DailyProcessor,
    DailyToDataFrame,
    OperatorProcessor,
    Scorer,
    SingleParamProcessor,
)
from post_analyzer.exporters import ExcelExporter


class PostAnalyzerApp:

    def __init__(self, config: AppConfig = None):
        self._config = config or AppConfig()
        self._scorer = Scorer(self._config.scoring_weights)

    def run(self):
        print("=" * 60)
        print("  Post Operator Performance Analyzer")
        print("=" * 60)

        # 1. بارگذاری
        df_call = CallLoader(self._config).load()
        panel_data = PanelLoader(self._config).load()

        # 2. پردازش روزانه
        daily_records = DailyProcessor(
            self._config, df_call, panel_data
        ).process()

        # 3. تبدیل روزانه به DataFrame
        df_daily = DailyToDataFrame.convert(daily_records)

        # 4. عملکرد اپراتورها + جمع کل
        df_operators = OperatorProcessor(
            self._config, daily_records, self._scorer
        ).process()

        # 5. عملکرد تک‌پارامتری
        df_single = self._build_single_param(df_operators)

        # 6. خروجی — با پاس دادن df_daily و df_operators برای نمودارها
        ExcelExporter(self._config.output_file).export(
            sheets={
                "گزارش روزانه": df_daily,
                "عملکرد اپراتورها": df_operators,
                "عملکرد تک‌پارامتری": df_single,
            },
            df_daily=df_daily,
            df_operators=df_operators,
        )

        # 7. خلاصه
        self._print_summary(df_operators)

    # ----- private -----

    def _build_single_param(self, df_operators: pd.DataFrame) -> pd.DataFrame:
        total_row = df_operators[df_operators["اپراتور"] == "جمع کل پست"]
        if len(total_row) == 0:
            return pd.DataFrame()

        tr = total_row.iloc[0]
        total_metrics = {
            "call_ratio": tr["نسبت تماس به فاکتور (%)"],
            "avg_gap_seconds": tr["میانگین فاصله بین تماس (ثانیه)"],
            "no_call_ratio": tr["نسبت فاکتور بدون تماس (%)"],
            "op_no_answer_ratio": tr["نسبت عدم پاسخگویی اپراتور (%)"],
            "coverage_pct": tr["درصد تماس پست (%)"],
            "reject_ratio": tr["نسبت رد (%)"],
            "approve_ratio": tr["نسبت تایید (%)"],
        }
        total_scores = self._scorer.compute_scores(total_metrics)

        return SingleParamProcessor(
            self._config.scoring_weights, total_scores, total_metrics
        ).process()

    def _print_summary(self, df_operators: pd.DataFrame):
        print(f"\n{'=' * 60}")
        print("  خلاصه عملکرد")
        print(f"{'=' * 60}")

        for _, row in df_operators.iterrows():
            label = row["اپراتور"]
            marker = "★" if label == "جمع کل پست" else "●"
            print(f"\n  {marker} {label}:")
            print(
                f"    روز فعال: {row['تعداد روز فعال']} | "
                f"کل تماس: {row['تعداد کل تماس']} | "
                f"یونیک: {row['تعداد شماره یونیک تماس']}"
            )
            print(
                f"    نسبت تماس/فاکتور: {row['نسبت تماس به فاکتور (%)']}% | "
                f"بدون تماس: {row['تعداد فاکتور بدون تماس']}"
            )
            print(
                f"    تایید: {row['نسبت تایید (%)']}% | "
                f"رد: {row['نسبت رد (%)']}%"
            )
            print(f"    ⭐ امتیاز کلی: {row['امتیاز کلی عملکرد']}")

        print(f"\n{'=' * 60}")
