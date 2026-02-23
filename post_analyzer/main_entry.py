"""نقطه ورود برای __main__.py"""

from .config import AppConfig, StatusWorkConfig, ScoringWeights
from app import PostAnalyzerApp


def main():
    config = AppConfig(
        input_file='../post.xlsx',
        output_file='../post_report.xlsx',
        target_operators=[
            'افشین دلبسته',
            'افسانه جوادی',
            'افسانه عسکری بقرآبادی',
            'حانیه اکبری',
        ],
        status_config=StatusWorkConfig(),
        scoring_weights=ScoringWeights(),
    )
    PostAnalyzerApp(config).run()
