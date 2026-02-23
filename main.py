#!/usr/bin/env python3
"""
نقطه ورود اصلی.
Usage:
    cd post_analyzer/..       # پوشه والد
    python -m post_analyzer   # اجرا به صورت ماژول
    # یا:
    python post_analyzer/main.py
"""

import sys
import os

# اطمینان از قرار گرفتن پوشه والد در مسیر
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from post_analyzer.config import AppConfig, StatusWorkConfig, ScoringWeights
from post_analyzer.app import PostAnalyzerApp


def main():
    config = AppConfig(
        input_file='post.xlsx',
        output_file='post_report.xlsx',
        target_operators=[
            'زهرا فرشباف',
            'افشین دلبسته',
            'افسانه جوادی',
            'افسانه عسکری بقرآبادی',
            'حانیه اکبری',
        ],
        status_config=StatusWorkConfig(
            status_seconds={
                'پاسخ داده': 60,
                'عدم پاسخگویی': 60,
                'عدم پاسخگویی اپراتور': 60,
                'مشغول بودن خط': 60,
                'لغو تماس': 60,
            },
            default_seconds=60,
        ),
        scoring_weights=ScoringWeights(
            call_ratio=1,
            avg_gap_seconds=1,
            no_call_invoice_ratio=1,
            operator_no_answer_ratio=1,
            call_coverage_pct=1,
            approve_ratio=1,
            reject_ratio=1,
        ),
    )

    app = PostAnalyzerApp(config)
    app.run()


if __name__ == '__main__':
    main()
