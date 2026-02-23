# post_analyzer/charts/chart_colors.py

"""
رنگ‌های ثابت برای هر اپراتور در نمودارها.
"""

# لیست رنگ‌ها — هر اپراتور یک رنگ ثابت می‌گیرد
OPERATOR_COLORS = [
    "4472C4",  # آبی
    "ED7D31",  # نارنجی
    "A5A5A5",  # خاکستری
    "FFC000",  # زرد
    "5B9BD5",  # آبی روشن
    "70AD47",  # سبز
    "264478",  # آبی تیره
    "9B59B6",  # بنفش
    "E74C3C",  # قرمز
    "1ABC9C",  # فیروزه‌ای
    "F39C12",  # طلایی
    "2ECC71",  # سبز روشن
]

# رنگ ویژه سطر "جمع کل پست"
TOTAL_COLOR = "FF0000"


def get_color(index: int) -> str:
    """رنگ اپراتور بر اساس ایندکس"""
    return OPERATOR_COLORS[index % len(OPERATOR_COLORS)]
